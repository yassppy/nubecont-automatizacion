package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"strings"
	"time"

	"api-app/models"
	"api-app/scraper"

	pw "github.com/mxschmitt/playwright-go"
)

type ValidateHandler struct {
	Browser pw.Browser
}

func NewValidateHandler(browser pw.Browser) *ValidateHandler {
	return &ValidateHandler{Browser: browser}
}

func (h *ValidateHandler) ValidateBatch(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
		return
	}

	start := time.Now()
	var batch models.BatchRequest

	if err := json.NewDecoder(r.Body).Decode(&batch); err != nil {
		http.Error(w, "Payload JSON inválido", http.StatusBadRequest)
		return
	}

	ctx, err := h.Browser.NewContext(pw.BrowserNewContextOptions{
		UserAgent: pw.String("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
		Locale:    pw.String("es-PE"),
	})
	if err != nil {
		http.Error(w, "Error al crear contexto de navegador", http.StatusInternalServerError)
		return
	}
	defer ctx.Close()

	page, err := ctx.NewPage()
	if err != nil {
		http.Error(w, "Error al crear pestaña", http.StatusInternalServerError)
		return
	}
	defer page.Close()

	results := make(map[string]models.DocumentResult)

	for _, doc := range batch.Documents {
		num := strings.TrimSpace(doc.NumDoc)
		tipo := strings.ToUpper(strings.TrimSpace(doc.TipoDoc))

		var res models.DocumentResult
		if tipo == "DNI" || (len(num) == 8 && tipo != "RUC") {
			log.Printf("🔍 Consultando SUNAT por DNI: %s", num)
			res = scraper.QueryDni(page, num)
		} else {
			log.Printf("🔍 Consultando SUNAT por RUC: %s", num)
			res = scraper.QueryRuc(page, num)
		}

		results[num] = res
	}

	resp := models.BatchResponse{
		TotalProcessed: len(results),
		DurationMs:     time.Since(start).Milliseconds(),
		Results:        results,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
