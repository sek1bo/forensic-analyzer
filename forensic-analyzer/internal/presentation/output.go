package presentation

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"forensic-analyzer/internal/domain"
)

// OutputJSON выводит результаты в формате JSON.
func OutputJSON(files []domain.FileData) {
	jsonData, err := json.MarshalIndent(files, "", "  ")
	if err != nil {
		log.Fatalf("Error marshalling JSON: %v", err)
	}
	fmt.Println(string(jsonData))
}

// OutputCSV выводит результаты в формате CSV.
func OutputCSV(files []domain.FileData) {
	writer := csv.NewWriter(os.Stdout)
	// Заголовок CSV
	header := []string{"Name", "Path", "Size", "Category", "Suspicious", "Metadata", "Analysis"}
	if err := writer.Write(header); err != nil {
		log.Fatalf("Error writing CSV header: %v", err)
	}
	// Запись данных по каждому файлу
	for _, file := range files {
		metadataJSON, _ := json.Marshal(file.Metadata)
		analysisJSON, _ := json.Marshal(file.Analysis)
		record := []string{
			file.Name,
			file.Path,
			fmt.Sprintf("%d", file.Size),
			file.Category,
			fmt.Sprintf("%t", file.Suspicious),
			string(metadataJSON),
			string(analysisJSON),
		}
		if err := writer.Write(record); err != nil {
			log.Fatalf("Error writing CSV record: %v", err)
		}
	}
	writer.Flush()
	if err := writer.Error(); err != nil {
		log.Fatalf("Error flushing CSV writer: %v", err)
	}
}
