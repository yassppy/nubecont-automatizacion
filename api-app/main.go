package main

import (
	"log"
	"net/http"

	"api-app/handlers"

	pw "github.com/mxschmitt/playwright-go"
)

func main() {
	log.Println("🔧 Iniciando Playwright...")
	globalPW, err := pw.Run()
	if err != nil {
		log.Fatalf("Error en pw.Run: %v", err)
	}

	globalBrowser, err := globalPW.Chromium.Launch(pw.BrowserTypeLaunchOptions{
		Headless: pw.Bool(true),
		Args: []string{
			"--disable-blink-features=AutomationControlled",
			"--no-sandbox",
			"--disable-dev-shm-usage",
		},
	})
	if err != nil {
		log.Fatalf("Error al lanzar Chromium: %v", err)
	}
	defer globalBrowser.Close()

	// Inyectar el navegador en los handlers
	validateHandler := handlers.NewValidateHandler(globalBrowser)

	http.HandleFunc("/api/v1/validar-lote", validateHandler.ValidateBatch)

	log.Println("🚀 Servidor listo en :7860")
	if err := http.ListenAndServe(":7860", nil); err != nil {
		log.Fatalf("Error servidor: %v", err)
	}
}
