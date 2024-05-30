import nibabel as nib
import pandas as pd
import os
import sys

def validate_voxel_size(voxel_size):
    validation = []
    for v in voxel_size:
        if v <= 0.7:
            validation.append("downsampling")
        elif 0.89 <= v <= 1.2:
            validation.append("valid")
        elif v >= 1.3:
            validation.append("invalid")
        else:
            validation.append("undefined")
    return validation

def check_isometric(voxel_size):
    max_diff = 0.3
    if (abs(voxel_size[0] - voxel_size[1]) <= max_diff and
        abs(voxel_size[1] - voxel_size[2]) <= max_diff and
        abs(voxel_size[0] - voxel_size[2]) <= max_diff):
        return "isometric"
    else:
        return "nonisometric"

def check_downsampling(voxel_validation):
    if "invalid" in voxel_validation:
        return "dontuse"
    elif "downsampling" in voxel_validation:
        return "downto"
    return "normal"

def extract_nifti_info(nifti_files):
    data = []

    for nifti_file in nifti_files:
        try:
            # Cargar la imagen NIfTI
            img = nib.load(nifti_file)
            
            # Obtener el tamaño del voxel (voxel size)
            voxel_size = img.header.get_zooms()[:3]
            voxel_validation = validate_voxel_size(voxel_size)
            isometric = check_isometric(voxel_size)
            downsampling_result = check_downsampling(voxel_validation)
            
            # Obtener el número de cortes (número de slices)
            num_slices = img.shape[2] if len(img.shape) > 2 else 1
            
            # Obtener el TR (Tiempo de Repetición)
            tr = img.header.get_zooms()[3] if len(img.header.get_zooms()) > 3 else "No especificado"
            
            # Añadir los datos a la lista
            data.append({
                "Archivo": os.path.basename(nifti_file),
                "Tamaño del voxel x": voxel_size[0],
                "Tamaño del voxel y": voxel_size[1],
                "Tamaño del voxel z": voxel_size[2],
                "Validación voxel x": voxel_validation[0],
                "Validación voxel y": voxel_validation[1],
                "Validación voxel z": voxel_validation[2],
                "Isometricidad": isometric,
                "Número de cortes": num_slices,
                "TR (Tiempo de Repetición)": tr,
                "Resultado": downsampling_result
            })
        except Exception as e:
            print(f"Error procesando el archivo {nifti_file}: {e}")

    # Crear un DataFrame de pandas
    df = pd.DataFrame(data)
    return df

def find_nifti_files(directory):
    nifti_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if ("T1" in file) and (file.endswith(".nii") or file.endswith(".nii.gz")):
                nifti_files.append(os.path.join(root, file))
    return nifti_files

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_al_directorio>")
        sys.exit(1)
    
    directory = sys.argv[1]
    nifti_files = find_nifti_files(directory)
    
    if not nifti_files:
        print("No se encontraron archivos NIfTI con 'T1' en el nombre en el directorio especificado.")
        sys.exit(1)
    
    df = extract_nifti_info(nifti_files)
    
    # Guardar el DataFrame en un archivo CSV
    output_csv = "nifti_info.csv"
    df.to_csv(output_csv, index=False)
    
    print(f"Información extraída y guardada en {output_csv}")
