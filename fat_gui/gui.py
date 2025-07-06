import tkinter as tk
import os
import json
import threading
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from repository.scanner import scan_files
from presentation.output import to_json, to_csv, to_pdf

def run_fat_gui():
    root = tk.Tk()
    root.title("FAT - Forensic Analysis Tool")
    root.geometry("800x700")
    root.configure(bg="#1e1e1e")

    selected_dir = {"path": ""}
    current_report = {"text": ""}

    settings_file = "settings.json"
    default_settings = {
        "enable_metadata": True,
        "enable_analysis": True,
        "enable_suspicious": True
    }

    def load_settings():
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return default_settings.copy()

    def save_settings(new_settings):
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(new_settings, f, indent=2)

    settings = load_settings()

#лого
    try:
        img = Image.open("fat_logo.png").resize((140, 140))
        logo = ImageTk.PhotoImage(img)
        tk.Label(root, image=logo, bg="#1e1e1e").pack(pady=(20, 10))
    except:
        tk.Label(root, text="[fat_logo.png not found]", fg="white", bg="#1e1e1e").pack(pady=10)

    tk.Label(root, text="FAT", fg="white", bg="#1e1e1e", font=("Arial", 26, "bold")).pack()
    tk.Label(root, text="Forensic Analysis Tool", fg="white", bg="#1e1e1e", font=("Arial", 12)).pack(pady=(0, 20))

    def create_button(text, command, bg="white", fg="black"):
        return tk.Button(
            root, text=text, command=command,
            font=("Arial", 12), bg=bg, fg=fg,
            activebackground=bg, activeforeground=fg,
            width=25, height=2, bd=0, relief="flat", highlightthickness=0
        )

    def choose_dir():
        path = filedialog.askdirectory()
        if path:
            selected_dir["path"] = path
            messagebox.showinfo("Directory Selected", f"✅ Selected folder:\n{path}")

    def run_analysis():
        if not selected_dir["path"]:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "Analysis started...\n")

        def analyze():
            files = scan_files(
                selected_dir["path"],
                enable_metadata=settings.get("enable_metadata", True),
                enable_analysis=settings.get("enable_analysis", False),
                enable_suspicious=settings.get("enable_suspicious", True)
            )
            report = to_json(files)
            current_report["text"] = report

            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, report)

        thread = threading.Thread(target=analyze)
        thread.start()

    def save_report():
        if not current_report["text"].strip():
            messagebox.showerror("Error", "Report is empty.")
            return

        filetypes = [
            ("Text Report", "*.txt"),
            ("CSV Report", "*.csv"),
            ("JSON Report", "*.json"),
            ("PDF Report", "*.pdf")
        ]
        filepath = filedialog.asksaveasfilename(filetypes=filetypes)

        if not filepath:
            return

        ext_map = {
            ".txt": "txt",
            ".csv": "csv",
            ".json": "json",
            ".pdf": "pdf"
        }

        selected_ext = None
        for ext in ext_map:
            if filepath.lower().endswith(ext):
                selected_ext = ext
                break

        if not selected_ext:
            desc = filedialog.asksaveasfilename(filetypes=filetypes).split(" ")[-1]
            if "csv" in desc.lower():
                selected_ext = ".csv"
            elif "json" in desc.lower():
                selected_ext = ".json"
            elif "pdf" in desc.lower():
                selected_ext = ".pdf"
            else:
                selected_ext = ".txt"
            filepath += selected_ext

        try:
            parsed = json.loads(current_report["text"])

            if selected_ext == ".csv":
                to_csv(parsed, filepath)
            elif selected_ext == ".json":
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, indent=2)
            elif selected_ext == ".pdf":
                to_pdf(parsed, filepath)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(current_report["text"])

            messagebox.showinfo("Success", f"Report saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def open_settings_window():
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")
        settings_window.geometry("300x220")
        settings_window.configure(bg="#1e1e1e")

        var_metadata = tk.BooleanVar(value=settings["enable_metadata"])
        var_analysis = tk.BooleanVar(value=settings["enable_analysis"])
        var_suspicious = tk.BooleanVar(value=settings["enable_suspicious"])

        def save_and_close():
            settings["enable_metadata"] = var_metadata.get()
            settings["enable_analysis"] = var_analysis.get()
            settings["enable_suspicious"] = var_suspicious.get()
            save_settings(settings)
            settings_window.destroy()

        tk.Checkbutton(settings_window, text="Enable Metadata Extraction", variable=var_metadata, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(settings_window, text="Enable Content Analysis", variable=var_analysis, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(settings_window, text="Enable Suspicious File Check", variable=var_suspicious, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack(anchor="w", padx=20, pady=5)

        tk.Button(settings_window, text="Save", command=save_and_close, bg="white", fg="black", width=15).pack(pady=15)

#кнопки
    create_button("New Analysis", choose_dir).pack(pady=5)
    create_button("Settings", open_settings_window).pack(pady=5)
    create_button("Start", run_analysis, bg="#3f65f2", fg="white").pack(pady=(10, 20))
    create_button("Save Report", save_report).pack(pady=(0, 10))
    
#окно вывода, чтоб не лагало
    nonlocal_output = scrolledtext.ScrolledText(root, width=90, height=20, bg="#2b2b2b", fg="white", insertbackground="white")
    nonlocal_output.pack(pady=10)
    output_box = nonlocal_output

    root.mainloop()
