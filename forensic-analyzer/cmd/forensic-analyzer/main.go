package main

import (
	"flag"
	"fmt"
	"log"

	"forensic-analyzer/internal/presentation"
	"forensic-analyzer/internal/repository"
)

func main() {
	// CLI-флаги
	dirPtr := flag.String("dir", ".", "Directory to scan")
	outputPtr := flag.String("output", "json", "Output format: json or csv")
	metadataPtr := flag.Bool("metadata", true, "Enable metadata extraction for images")
	analysisPtr := flag.Bool("analysis", false, "Enable content analysis for documents/text files")
	suspiciousPtr := flag.Bool("suspicious", true, "Enable suspicious file check")
	flag.Parse()

	fmt.Printf("Scanning directory: %s\n", *dirPtr)
	files, err := repository.ScanFiles(*dirPtr, *metadataPtr, *analysisPtr, *suspiciousPtr)
	if err != nil {
		log.Fatalf("Error scanning files: %v", err)
	}

	// Вывод результата в выбранном формате
	if *outputPtr == "json" {
		presentation.OutputJSON(files)
	} else if *outputPtr == "csv" {
		presentation.OutputCSV(files)
	} else {
		fmt.Println("Unsupported output format. Use 'json' or 'csv'.")
	}
}
