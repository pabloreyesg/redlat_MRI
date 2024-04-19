import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def run_c3d_info(file_path):
    command = ["c3d", file_path, "-info"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def browse_folder(root):  # Añadimos root como argumento
    folder_path = filedialog.askdirectory()
    if folder_path:
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, "Ejecutando, por favor espere...\n")
        root.update()  # Ahora root es pasado como argumento
        report_file_path = os.path.join(folder_path, "c3d_info_report.txt")
        with open(report_file_path, "w") as report_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".nii.gz") and "T1" in file:
                        file_path = os.path.join(root, file)
                        info = run_c3d_info(file_path)
                        report_file.write(f"File: {file_path}\n")
                        report_file.write(info)
                        report_file.write("\n\n")
        info_text.insert(tk.END, f"Reporte generado en: {report_file_path}")

# Crear la ventana principal
root = tk.Tk()
root.title("C3D Info GUI")

# Botón para seleccionar la carpeta
browse_button = tk.Button(root, text="Seleccionar carpeta", command=lambda: browse_folder(root))
browse_button.pack(pady=10)

# Texto de salida
info_text = tk.Text(root, height=20, width=80)
info_text.pack(padx=10, pady=10)

root.mainloop()
