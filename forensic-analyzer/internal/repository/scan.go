package repository

import (
	"os"
	"path/filepath"

	"forensic-analyzer/internal/domain"
	"forensic-analyzer/internal/usecase"
)

// ScanFiles рекурсивно сканирует указанную директорию и собирает информацию о файлах.
// Флаги enableMetadata, enableAnalysis и enableSuspicious позволяют включать или отключать соответствующие функции.
func ScanFiles(rootPath string, enableMetadata, enableAnalysis, enableSuspicious bool) ([]domain.FileData, error) {
	var files []domain.FileData
	err := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err // Пропускаем файлы, по которым возникли ошибки доступа
		}
		if !info.IsDir() {
			category := usecase.ClassifyFile(info.Name())
			var metadata map[string]string
			if enableMetadata && category == "Image" {
				metadata = usecase.ExtractMetadata(path)
			}
			var analysis map[string]interface{}
			if enableAnalysis && (category == "Document" || filepath.Ext(path) == ".txt") {
				analysis = usecase.AnalyzeFileContent(path, category)
			}
			suspicious := false
			if enableSuspicious {
				suspicious = usecase.CheckSuspicious(path, category)
			}
			fileData := domain.FileData{
				Name:       info.Name(),
				Path:       path,
				Size:       info.Size(),
				Category:   category,
				Metadata:   metadata,
				Suspicious: suspicious,
				Analysis:   analysis,
			}
			files = append(files, fileData)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}
	return files, nil
}
