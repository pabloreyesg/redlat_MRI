# Autor: [Pablo Reyes]
# Fecha: [24/04/2023]
# Descripción: [Obtencion de métricas desde Json para revision de calidad]



# Cargar la librería "jsonlite"
library(jsonlite)



# Cargar el archivo JSON de la funcional

archivo_json <- fromJSON("/media/pablo/Aldebaran/mri_redlat/mriqc_ma/sub-MA201/func/sub-MA201_task-rest_run-1_bold.json")

# Ver la estructura del archivo
str(archivo_json)


# Ver los nombres de los elementos del archivo
names(archivo_json)

# Acceder a un elemento específico

dvars <- archivo_json$dvars_nstd #porcentaje de delta de cambio en BOLD
fd_perc <- archivo_json$fd_perc # si el resultado esta entre 0 - 25 no se revisa, si el resultado esta entre 26-50 es optativo y es importante un sistema de corrección, mas de 50 % se requerira implementar sistemas de correccion sio el valor es
tsnr <- archivo_json$tsnr # valores muy bajos (en compración con la media global) deben revisarse
bidsmeta <- archivo_json$bids_meta #temporal
idsub <- bidsmeta$subject_id # obtencion del id
df <- data.frame(idsub, dvars, fd_perc, tsnr)

# Guardar los datos en un archivo CSV
write.csv(archivo_json, "ruta/a/tu/archivo.csv", row.names = FALSE)
