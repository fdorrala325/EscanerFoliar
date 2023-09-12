import cv2
import numpy as np
import re


def area_foliar(ruta_imagen, dpi, ruta_ImagenArea):
	image = cv2.imread(ruta_imagen)
	image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
		
	# Convertir la imagen a escala a grises 
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Crear una máscara binaria identificando píxeles blancos (Segmentación)
	_, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

	# Invertir la máscara para resaltar la hoja como primer plano 
	thresholded_inverted = cv2.bitwise_not(thresholded)

	# Encontrar los contornos en la máscara
	contours, _ = cv2.findContours(thresholded_inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#Encontrar el contorno más grande
	contorno_mayor = max(contours, key=cv2.contourArea)

	# Dibujar el contorno mayor en una copia de la imagen original
	imagen_contorno_mayor = image.copy()
	cv2.drawContours(imagen_contorno_mayor, [contorno_mayor], -1, (0, 0, 255), 20)

	# Calcular el área del contorno más grande (área de la hoja)
	area_hoja_pixeles = cv2.contourArea(contorno_mayor)

	# Convertir el area en pixeles a cm^2
		# Area hoja cm^2 = (Area Pixeles)*(2.54cm/pulgada)^2/(dpi)^2
	area_hoja_cm2 = (area_hoja_pixeles)*(2.54 ** 2)/(dpi ** 2)

	# Redondea el area a tres decimales
	area_redondeada = round(area_hoja_cm2, 3)

	# Crear una imagen con el contorno mayor dibujado y el área de la hoja en cm^2
	imagen_area = cv2.putText(imagen_contorno_mayor, f"Area de la hoja: {area_redondeada:.2f} cm^2", (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 0, 0), 2, cv2.LINE_AA)

	#Guardar la imagen 
	cv2.imwrite(ruta_ImagenArea, imagen_area)

	return area_redondeada


def guardar_Area(area, numeroHoja_actual, ruta_area):
	
	Dato_area = f'Area Foliar de la Hoja #{numeroHoja_actual} : {area}'
	hoja_existente = None
	vacio = True

	#Leer Archivo de texto para obtener la hoja actual 
	try:
		with open(ruta_area, 'r') as archivo:
			lineas = archivo.readlines()
					
			if lineas:  # Verificar si el contenido no está vacío
				ultima_linea = lineas[-1]
				hoja_existente = re.search(r'#(\d+)', ultima_linea)
				hoja_existente = int(hoja_existente.group(1))
				vacio = False
			else:
				vacio = True
				print(vacio)
		
		if hoja_existente is not None and hoja_existente == numeroHoja_actual:
			#Sobreescribir en el archivo de texto el valor del area si la hoja existe 
			with open(ruta_area, 'r+') as archivo:
				lineas = archivo.readlines()
				lineas[-1] = Dato_area + '\n'
				archivo.seek(0)
				archivo.writelines(lineas)
				print(f"Se sobreescribio el dato area para Hoja-{numeroHoja_actual}")
		else:
			# Agregar en el archivo de texto el nuevo valor del area si la hoja no existe
			with open(ruta_area, 'a') as archivo:
				archivo.write(Dato_area + '\n')
			print("Se agrego nuevo dato area")
		
	except FileNotFoundError:
		print('Error al guardar dato del area')
