package domain

// FileData представляет сущность файла для дальнейшей классификации.
type FileData struct {
	Name       string                 `json:"name"`
	Path       string                 `json:"path"`
	Size       int64                  `json:"size"`
	Category   string                 `json:"category"`
	Metadata   map[string]string      `json:"metadata,omitempty"`
	Suspicious bool                   `json:"suspicious"`
	Analysis   map[string]interface{} `json:"analysis,omitempty"`
}
