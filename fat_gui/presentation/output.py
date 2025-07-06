import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрируем кириллический шрифт
pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

def to_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False)

def to_csv(data, filepath):
    if not data:
        return

    keys = ["name", "path", "size", "category", "suspicious", "metadata", "analysis"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for entry in data:
            row = {
                k: json.dumps(entry.get(k, ""), ensure_ascii=False)
                if isinstance(entry.get(k), dict) else entry.get(k, "")
                for k in keys
            }
            writer.writerow(row)

def wrap_text(text, max_width, font_name="DejaVu", font_size=10):
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if stringWidth(test_line, font_name, font_size) < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def to_pdf(data, filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("DejaVu", 14)
    c.drawString(40, y, "FAT - Forensic Analysis Tool Report")
    y -= 30

    c.setFont("DejaVu", 10)
    max_width = width - 80

    for i, file in enumerate(data, 1):
        lines = [
            f"{i}. File: {file.get('name', 'N/A')}",
            f"Path: {file.get('path', '')}",
            f"Size: {file.get('size', 0)} bytes",
            f"Category: {file.get('category', '')}",
            f"Suspicious: {file.get('suspicious', '')}",
        ]

        if file.get('metadata'):
            lines.append(f"Metadata: {json.dumps(file['metadata'], ensure_ascii=False)}")
        if file.get('analysis'):
            lines.append(f"Analysis: {json.dumps(file['analysis'], ensure_ascii=False)}")

        for line in lines:
            wrapped = wrap_text(line, max_width)
            for wrapped_line in wrapped:
                c.drawString(60, y, wrapped_line)
                y -= 12
                if y < 100:
                    c.showPage()
                    c.setFont("DejaVu", 10)
                    y = height - 40
            y -= 4

        y -= 8

    c.save()
