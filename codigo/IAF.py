import re

#Función para calcular el índice de área foliar de un cultivo 

def calcularIAF(ruta_archivo):
    # Inicializa una variable para almacenar la suma de las áreas
    suma_areas = 0.0
    
	# Dato establecido sobre el area que abarca la superficie del cultivo 
    largo = 0.8
    ancho = 0.2
    factor_area_cultivo = largo*ancho*10000

    # Lee el archivo de Áreas y suma las áreas de las hojas
    try:
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                # Divide la línea en partes usando el carácter ':' como separador
                partes = linea.strip().split(':')
                if len(partes) == 2:
                    # La segunda parte debe ser el valor de "area"
                    area = float(partes[1])
                    suma_areas += area
    except FileNotFoundError:
        print(f'El archivo {ruta_archivo} no se encontró.')
    except Exception as e:
        print(f'Ocurrió un error al leer el archivo: {e}')

	#Cálculo del índice de área foliar 
    IAF = (suma_areas)/(factor_area_cultivo)

    # Redondea el IAF a tres decimales
    resultado_redondeado = round(IAF, 3)
    print(resultado_redondeado)

    return resultado_redondeado

#Función para guardar el dato de IAF en un archivo de texto 

def guardar_IAF(IAF,numeroCultivo_actual, ruta_IAF):
    
	Dato_IAF = f'Indice de Area Foliar del Cultivo #{numeroCultivo_actual} : {IAF}'
	Cultivo_existente = None
	vacio = True

	#Leer y guardar en el archivo de Indice de area foliar
	try:
		with open(ruta_IAF, 'r') as archivo:
			lineas = archivo.readlines()
					
			if lineas:  # Verificar si el contenido no está vacío
				
				ultima_linea = lineas[-1]
				Cultivo_existente = re.search(r'#(\d+)', ultima_linea)
				Cultivo_existente = int(Cultivo_existente.group(1))
			else:
				vacio = True
				print(vacio)
		

		if Cultivo_existente is not None and Cultivo_existente == numeroCultivo_actual:
			# Sobrescribir la última línea con el nuevo valor
			with open(ruta_IAF, 'r+') as archivo:
				lineas = archivo.readlines()
				lineas[-1] = Dato_IAF + '\n'
				archivo.seek(0)
				archivo.writelines(lineas)
				print(f"Se sobreescribio el dato IAF para el cultivo-{numeroCultivo_actual}")
		else:
			# Agregar el nuevo valor al archivo
			with open(ruta_IAF, 'a') as archivo:
				archivo.write(Dato_IAF + '\n')
			print("Se agrego nuevo dato IAF")
		
	except FileNotFoundError:
		print('Error al guardar dato del IAF')
