import os
import hashlib
import requests
import time
import mimetypes

# ключ с моего акка вирустотал
VT_API_KEY = "cc9ad007845bc1ca65669f3724b0cffecb38d63e4e5bc6031888450193a65127"

def classify_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    types = {
        "Document": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"},
        "Image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"},
        "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
        "Video": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
        "Executable": {".exe", ".dll", ".bat", ".sh", ".bin"},
        "Archive": {".zip", ".rar", ".tar", ".gz", ".7z"}
    }
    for category, extensions in types.items():
        if ext in extensions:
            return category
    return "Other"

def extract_metadata(file_path):
    metadata = {}
    try:
        stat = os.stat(file_path)
        metadata["Size (bytes)"] = stat.st_size
        metadata["Modified Time"] = time.ctime(stat.st_mtime)
        metadata["Created Time"] = time.ctime(stat.st_ctime)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            metadata["MIME Type"] = mime_type

        with open(file_path, "rb") as f:
            data = f.read()
            metadata["MD5"] = hashlib.md5(data).hexdigest()
            metadata["SHA1"] = hashlib.sha1(data).hexdigest()
    except Exception as e:
        metadata["Error"] = str(e)
    return metadata

def analyze_file_content(file_path, category):
    analysis = {}
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in {".txt", ".log", ".md", ".csv"} or category == "Document":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                words = text.split()
                analysis["Word Count"] = len(words)
        else:
            with open(file_path, "rb") as f:
                data = f.read(64)
                analysis["File Header (hex)"] = data.hex()
    except Exception as e:
        analysis["Error"] = str(e)
    return analysis

def hash_file(filepath, algo="sha256"):
    h = hashlib.new(algo)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def is_suspicious(file_path, category):
    if category != "Executable":
        return False

    try:
        file_hash = hash_file(file_path)
    except Exception:
        return True  # не удалось прочитать — подозрительно

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            return malicious > 0 or suspicious > 0
        elif response.status_code == 404:
            return False  # файл не найден в базе — считаем чистым
        else:
            return True  # при других ошибках — помечаем как подозрительный
    except Exception:
        return True  # при проблемах с API — считаем подозрительным
