import os
import shutil
import subprocess
from LCD import *

# Ruta de origen en la tarjeta de almacenamiento
ruta_origen = "/media/Daniel/disk/DCIM/100MEDIA"  

def recibir_datos(ruta_destino, nombre_imagen):

	# Verificar si la carpeta de destino existe
	if not os.path.exists(ruta_destino):
		 print("No se encuentra la carpeta") # Crea la carpeta de destino si no existe

	try:
		# Mover todos los archivos desde la carpeta de origen a la carpeta de destino
		for archivo in os.listdir(ruta_origen):
			ruta_archivo_origen = os.path.join(ruta_origen, archivo)
			if os.path.isfile(ruta_archivo_origen):
				ruta_archivo_destino = os.path.join(ruta_destino, nombre_imagen)
				shutil.move(ruta_archivo_origen, ruta_archivo_destino)
		print("Archivos movido exitosamente")
	except Exception as e:
		print("Error al mover archivos:", str(e))

	try:
		# Ejecutar el comando para desmontar la tarjeta SD
		comando = ['sudo', 'umount', "/media/Daniel/disk"]
		subprocess.run(comando, check=True)

		print("Tarjeta SD desmontada con éxito.")
	except Exception as e:
		print("Error al desmontar la tarjeta SD:", str(e))

def transferir_datos(ruta_origen_rasp, ruta_destino_sd):
	try:
		
		# Copiar todos los archivos desde la carpeta de origen a la carpeta de destino
		shutil.copytree(ruta_origen_rasp, ruta_destino_sd, dirs_exist_ok=True)
		print("Archivos movido exitosamente")
		mostrar_lcd("Transfer.", "Completada")
	except Exception as e:
		print("Error al copiar archivos:", str(e))

	try:
		# Ejecutar el comando para desmontar la tarjeta SD
		comando = ['sudo', 'umount', "/media/Daniel/disk"]
		subprocess.run(comando, check=True)

		print("Tarjeta SD desmontada con éxito.")
	except Exception as e:
		print("Error al desmontar la tarjeta SD:", str(e))
