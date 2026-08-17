package scraper

import (
	"fmt"
	"strings"
	"time"

	pw "github.com/mxschmitt/playwright-go"
	"api-app/models"
)

const sunatFrameURL = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp"

func QueryRuc(page pw.Page, ruc string) models.DocumentResult {
	var dialogMessage string
	page.OnDialog(func(d pw.Dialog) {
		dialogMessage = d.Message()
		_ = d.Dismiss()
	})

	if err := navigateToSunat(page); err != nil {
		return models.DocumentResult{NumDoc: ruc, Success: false, Error: err.Error()}
	}

	_ = page.Click("#btnPorRuc")
	_ = page.Fill("#txtRuc", ruc)
	if err := page.Click("#btnAceptar"); err != nil {
		return models.DocumentResult{NumDoc: ruc, Success: false, Error: "Error al presionar Buscar: " + err.Error()}
	}

	time.Sleep(200 * time.Millisecond)
	if dialogMessage != "" {
		return models.DocumentResult{NumDoc: ruc, Success: false, Error: "SUNAT: " + dialogMessage}
	}

	_, _ = page.WaitForSelector(".list-group, .panel, .alert", pw.PageWaitForSelectorOptions{
		Timeout: pw.Float(8000),
	})

	nombre, estado, condicion, errExtract := extractRucDataFromDOM(page)
	if errExtract != nil {
		return models.DocumentResult{NumDoc: ruc, Success: false, Error: errExtract.Error()}
	}

	return models.DocumentResult{
		NumDoc:    ruc,
		Nombre:    nombre,
		Estado:    estado,
		Condicion: condicion,
		Success:   true,
	}
}

func QueryDni(page pw.Page, dni string) models.DocumentResult {
	var dialogMessage string
	page.OnDialog(func(d pw.Dialog) {
		dialogMessage = d.Message()
		_ = d.Dismiss()
	})

	if err := navigateToSunat(page); err != nil {
		return models.DocumentResult{NumDoc: dni, Success: false, Error: err.Error()}
	}

	_ = page.Click("#btnPorDocumento")
	_ = page.Fill("#txtNumeroDocumento", dni)
	if err := page.Click("#btnAceptar"); err != nil {
		return models.DocumentResult{NumDoc: dni, Success: false, Error: "Error al presionar Buscar: " + err.Error()}
	}

	time.Sleep(200 * time.Millisecond)
	if dialogMessage != "" {
		return models.DocumentResult{NumDoc: dni, Success: false, Error: "SUNAT: " + dialogMessage}
	}

	_, _ = page.WaitForSelector("a.aRucs, .panel, .alert, div.list-group-item", pw.PageWaitForSelectorOptions{
		Timeout: pw.Float(8000),
	})

	bodyText, _ := page.TextContent("body")
	if strings.Contains(bodyText, "NO REGISTRA un número de RUC") {
		return models.DocumentResult{
			NumDoc:  dni,
			Success: false,
			Error:   fmt.Sprintf("El Sistema RUC NO REGISTRA un número de RUC para el DNI %s consultado.", dni),
		}
	}

	rucLink := page.Locator("a.aRucs")
	if count, _ := rucLink.Count(); count > 0 {
		if err := rucLink.First().Click(); err != nil {
			return models.DocumentResult{NumDoc: dni, Success: false, Error: "Error al abrir detalle del RUC: " + err.Error()}
		}

		_, _ = page.WaitForSelector(".list-group, .panel", pw.PageWaitForSelectorOptions{
			Timeout: pw.Float(8000),
		})
	} else {
		return models.DocumentResult{NumDoc: dni, Success: false, Error: "No se encontró resultado para el DNI especificado"}
	}

	nombre, estado, condicion, errExtract := extractRucDataFromDOM(page)
	if errExtract != nil {
		return models.DocumentResult{NumDoc: dni, Success: false, Error: errExtract.Error()}
	}

	return models.DocumentResult{
		NumDoc:    dni,
		Nombre:    nombre,
		Estado:    estado,
		Condicion: condicion,
		Success:   true,
	}
}

func navigateToSunat(page pw.Page) error {
	var err error
	for i := 0; i < 2; i++ {
		_, err = page.Goto(sunatFrameURL, pw.PageGotoOptions{
			WaitUntil: pw.WaitUntilStateDomcontentloaded,
			Timeout:   pw.Float(15000),
		})
		if err == nil {
			return nil
		}
		time.Sleep(300 * time.Millisecond)
	}
	return fmt.Errorf("error al cargar SUNAT: %v", err)
}

func extractRucDataFromDOM(page pw.Page) (nombre, estado, condicion string, err error) {
	if alertLoc := page.Locator(".alert, #msgError, .error"); alertLoc != nil {
		if count, _ := alertLoc.Count(); count > 0 {
			if txt, _ := alertLoc.First().TextContent(); strings.TrimSpace(txt) != "" {
				txtClean := cleanText(txt)
				if strings.Contains(strings.ToLower(txtClean), "no existe") || strings.Contains(strings.ToLower(txtClean), "no valido") {
					return "", "", "", fmt.Errorf("RUC NO REGISTRADO O INVALIDO")
				}
			}
		}
	}

	rucRow := page.Locator("div.list-group-item:has(h4:has-text('Número de RUC')) .col-sm-7")
	if count, _ := rucRow.Count(); count > 0 {
		rawText, _ := rucRow.First().TextContent()
		cleanRaw := cleanText(rawText)

		if idx := strings.Index(cleanRaw, "-"); idx != -1 {
			nombre = strings.TrimSpace(cleanRaw[idx+1:])
		} else {
			nombre = cleanRaw
		}
	}

	estadoLoc := page.Locator("div.list-group-item:has(h4:has-text('Estado del Contribuyente')) .col-sm-7")
	if count, _ := estadoLoc.Count(); count > 0 {
		txt, _ := estadoLoc.First().TextContent()
		estado = cleanText(txt)
	}

	condLoc := page.Locator("div.list-group-item:has(h4:has-text('Condición del Contribuyente')) .col-sm-7")
	if count, _ := condLoc.Count(); count > 0 {
		txt, _ := condLoc.First().TextContent()
		condicion = cleanText(txt)
	}

	if nombre == "" {
		return "", "", "", fmt.Errorf("no se pudo extraer la información del documento")
	}

	return nombre, estado, condicion, nil
}

func cleanText(s string) string {
	s = strings.ReplaceAll(s, "\n", " ")
	s = strings.ReplaceAll(s, "\r", " ")
	s = strings.ReplaceAll(s, "\t", " ")
	s = strings.ReplaceAll(s, "\u00a0", " ")
	for strings.Contains(s, "  ") {
		s = strings.ReplaceAll(s, "  ", " ")
	}
	return strings.TrimSpace(s)
}
