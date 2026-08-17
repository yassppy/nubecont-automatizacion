package models

type DocumentRequest struct {
	NumDoc  string `json:"num_doc"`
	TipoDoc string `json:"tipo_doc"`
}

type BatchRequest struct {
	Documents []DocumentRequest `json:"documents"`
}

type DocumentResult struct {
	NumDoc    string `json:"num_doc"`
	Nombre    string `json:"nombre"`
	Estado    string `json:"estado"`
	Condicion string `json:"condicion"`
	Success   bool   `json:"success"`
	Error     string `json:"error,omitempty"`
}

type BatchResponse struct {
	TotalProcessed int                       `json:"total_processed"`
	DurationMs     int64                     `json:"duration_ms"`
	Results        map[string]DocumentResult `json:"results"`
}
