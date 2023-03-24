# Autor: [Pablo Reyes]
# Correo: [pabloreyesg@gmail.com]
# Fecha: [24/04/2023]
# Descripción: [Obtencion de métricas desde Json para revision de calidad para varios sujetos, se debe tener preparado una carpeta con todos los archivos json]



# Cargar la librería "jsonlite"
library(jsonlite)

# definir como folder de trabajo la carpeta donde se encuentran todos los archivos JSON

setwd("/media/pablo/Aldebaran/mri_redlat/mriqc_ma/json")

# Definir una función para extraer el título y el autor de un archivo JSON
extraer_info <- function(nombre_archivo) {
  # Cargar el archivo JSON
  archivo_json <- fromJSON(nombre_archivo)
  
  # Extraer el título y el autor
  dvars <- archivo_json$dvars_nstd #porcentaje de delta de cambio en BOLD
  fd_perc <- archivo_json$fd_perc # si el resultado esta entre 0 - 25 no se revisa, si el resultado esta entre 26-50 es optativo y es importante un sistema de corrección, mas de 50 % se requerira implementar sistemas de correccion sio el valor es
  tsnr <- archivo_json$tsnr # valores muy bajos (en compración con la media global) deben revisarse
  bidsmeta <- archivo_json$bids_meta #temporal
  idsub <- bidsmeta$subject_id # obtencion del id
  
  # Devolver un vector con el título y el autor
  return(c(idsub, dvars, fd_perc, tsnr))
}

# Obtener una lista de los nombres de los archivos JSON
archivos <- list.files("/media/pablo/Aldebaran/mri_redlat/mriqc_ma/json", pattern = "*.json")

# Aplicar la función a cada archivo y combinar los resultados en un dataframe
resultados <- do.call(rbind, lapply(archivos, extraer_info))

# Nombrar las columnas del dataframe
colnames(resultados) <- c("idsub", "dvars", "fd_perc", "tsnr")

# Ver el dataframe resultante
resultados


#guardar informacion
save(resultados, file = "calidadfunc.R")
write.csv(resultados, file = "calidadfunc", row.names = FALSE)


