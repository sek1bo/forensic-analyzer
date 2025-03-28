package usecase

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

// ClassifyFile определяет категорию файла по его расширению.
func ClassifyFile(fileName string) string {
	ext := strings.ToLower(filepath.Ext(fileName))
	documentExt := map[string]bool{
		".pdf": true, ".doc": true, ".docx": true, ".txt": true,
		".xls": true, ".xlsx": true, ".ppt": true, ".pptx": true, ".odt": true,
	}
	imageExt := map[string]bool{
		".jpg": true, ".jpeg": true, ".png": true, ".gif": true, ".bmp": true, ".tiff": true,
	}
	audioExt := map[string]bool{
		".mp3": true, ".wav": true, ".flac": true, ".aac": true, ".ogg": true,
	}
	videoExt := map[string]bool{
		".mp4": true, ".avi": true, ".mkv": true, ".mov": true, ".wmv": true, ".flv": true, ".webm": true,
	}
	executableExt := map[string]bool{
		".exe": true, ".dll": true, ".bat": true, ".sh": true, ".bin": true,
	}
	archiveExt := map[string]bool{
		".zip": true, ".rar": true, ".tar": true, ".gz": true, ".7z": true,
	}

	switch {
	case documentExt[ext]:
		return "Document"
	case imageExt[ext]:
		return "Image"
	case audioExt[ext]:
		return "Audio"
	case videoExt[ext]:
		return "Video"
	case executableExt[ext]:
		return "Executable"
	case archiveExt[ext]:
		return "Archive"
	default:
		return "Other"
	}
}

// ExtractMetadata пытается извлечь метаданные из файла, если это изображение.
// Для демонстрации возвращаются симулированные данные. Для реального анализа можно использовать библиотеку goexif.
func ExtractMetadata(filePath string) map[string]string {
	metadata := make(map[string]string)
	metadata["Info"] = "Simulated metadata extraction"
	return metadata
}

// AnalyzeFileContent проводит простой анализ содержимого для документов (например, подсчёт количества слов).
func AnalyzeFileContent(filePath string, category string) map[string]interface{} {
	analysis := make(map[string]interface{})
	if category == "Document" || strings.ToLower(filepath.Ext(filePath)) == ".txt" {
		data, err := ioutil.ReadFile(filePath)
		if err == nil {
			text := string(data)
			words := strings.Fields(text)
			analysis["WordCount"] = len(words)
		}
	}
	return analysis
}

// CheckSuspicious проводит простую эвристику для определения «подозрительности» файла.
func CheckSuspicious(filePath string, category string) bool {
	if category == "Executable" {
		if strings.Contains(strings.ToLower(filePath), "test") {
			return true
		}
		info, err := os.Stat(filePath)
		if err == nil && info.Size() < 10*1024 {
			return true
		}
	}
	return false
}
