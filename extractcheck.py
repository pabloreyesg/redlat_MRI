import json
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para buscar archivos JSON recursivamente
def buscar_archivos_json(directorio):
    archivos_json = []
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.endswith(".json"):
                archivos_json.append((root, file, os.path.join(root, file)))  # Guardar el nombre del directorio y del archivo
    return archivos_json

# Función para manejar el botón de selección de directorio
def seleccionar_directorio():
    directorio_principal = filedialog.askdirectory()
    directorio_entry.delete(0, tk.END)
    directorio_entry.insert(0, directorio_principal)

# Función principal para extraer información de archivos JSON
def extraer_info():
    directorio = directorio_entry.get()

    # Verificar si el directorio está vacío o no existe
    if not directorio or not os.path.exists(directorio):
        messagebox.showerror("Error", "El directorio no es válido.")
        return

    # Buscar archivos JSON recursivamente
    archivos_json_encontrados = buscar_archivos_json(directorio)

    # Lista para almacenar la información extraída de cada archivo con el nombre del directorio y del archivo
    extracted_info_list = []

    # Iterar sobre los archivos encontrados
    for directory, filename, filepath in archivos_json_encontrados:
        try:
            with open(filepath) as file:
                data = json.load(file)

                # Verifica si las claves están presentes en el archivo
                keys_to_extract = ["Manufacturer", "ManufacturersModelName", "InstitutionName", "ScanningSequence", "SliceThickness", "EchoTime","RepetitionTime","FlipAngle","PhaseEncodingDirection","SpacingBetweenSlices"]
                extracted_info = {
                    "Directory": directory,  # Agregar el nombre del directorio al resultado
                    "FileName": filename  # Agregar el nombre del archivo al resultado
                }

                # Verificar si el nombre del archivo contiene ciertas palabras clave
                if "T1" in filename:
                    extracted_info["ScanType"] = "T1"
                elif "T2" in filename:
                    extracted_info["ScanType"] = "T2"
                elif "bold" in filename:
                    extracted_info["ScanType"] = "BOLD"
                elif "dwi" in filename:
                    extracted_info["ScanType"] = "DWI"
                else:
                    extracted_info["ScanType"] = "Otro"

                for key in keys_to_extract:
                    if key in data:
                        extracted_info[key] = data[key]
                    else:
                        extracted_info[key] = "NA"

                # Agregar lógica adicional para SliceThickness
                if extracted_info["ScanType"] == "T1":
                    slice_thickness = float(extracted_info.get("SliceThickness", 0))
                    if 0.9 <= slice_thickness <= 1.2:
                        extracted_info["SliceValidity"] = "valid"
                    elif 0.4 <= slice_thickness <= 0.6:
                        extracted_info["SliceValidity"] = "downsampling"
                    elif slice_thickness > 1.3:
                        extracted_info["SliceValidity"] = "unvalid"
                    else:
                        extracted_info["SliceValidity"] = "Otro"
                else:
                    extracted_info["SliceValidity"] = "N/A"

                extracted_info_list.append(extracted_info)
        except json.JSONDecodeError:
            # Archivo JSON dañado o vacío
            messagebox.showwarning("Advertencia", f"El archivo JSON '{filename}' en '{directory}' no se pudo leer correctamente.")

    # Escribe la información en un archivo CSV
    output_file = 'informacion_extraida.csv'
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Directory", "FileName", "ScanType", "SliceValidity"] + keys_to_extract  # Agregar el nombre del directorio y del archivo como encabezados
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for info in extracted_info_list:
            writer.writerow(info)

    messagebox.showinfo("Finalizado", f"Se ha exportado la información de los archivos JSON al archivo '{output_file}'")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Extracción de Información de Archivos JSON")

# Etiqueta y campo de entrada para el directorio principal
directorio_label = tk.Label(root, text="Directorio principal:")
directorio_label.pack()
directorio_entry = tk.Entry(root)
directorio_entry.pack()

# Botón para seleccionar el directorio
seleccionar_button = tk.Button(root, text="Seleccionar Directorio", command=seleccionar_directorio)
seleccionar_button.pack()

# Botón para iniciar el proceso de extracción
extraer_button = tk.Button(root, text="Extraer Información", command=extraer_info)
extraer_button.pack()

root.mainloop()
