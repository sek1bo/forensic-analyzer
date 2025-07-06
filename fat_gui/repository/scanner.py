import os
from domain.filedata import FileData
from usecase.classifier import classify_file, extract_metadata, analyze_file_content, is_suspicious

def scan_files(root_path, enable_metadata=True, enable_analysis=False, enable_suspicious=True):
    results = []

    for dirpath, _, filenames in os.walk(root_path):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                stat = os.stat(path)
            except Exception:
                continue  # пропускаем файлы с ошибками

            category = classify_file(name)

            file_data = {
                "name": name,
                "path": path,
                "size": stat.st_size,
                "category": category,
            }

            if enable_metadata:
                file_data["metadata"] = extract_metadata(path)

            if enable_analysis:
                file_data["analysis"] = analyze_file_content(path, category)

            if enable_suspicious:
                file_data["suspicious"] = is_suspicious(path, category)

            results.append(file_data)

    return results
