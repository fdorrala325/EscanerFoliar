import os

#Funcion para obtener el nombre y el numero del cultivo actual del sistema 
def  numero_nombre_cultivo():
    try:
        with open("contador.txt", "r") as file:
            contenido = file.read()
            if contenido.strip():  # Verificar si el contenido no está vacío
                numero_cultivo = int(contenido)
            else:
                numero_cultivo = 0
            file.close()
    except FileNotFoundError:
        numero_cultivo = 0

    nombre_carpeta_cultivo = f"Cultivo-{numero_cultivo}"

    return numero_cultivo, nombre_carpeta_cultivo

#Funcion para obtener el nombre y el numero de la hoja actual del sistema 
def numero_nombre_hoja(carpeta_cultivo):
    try:
        with open(carpeta_cultivo + "/Contador_hojas.txt", "r") as file:
            contenido = file.read()
            if contenido.strip():  # Verificar si el contenido no está vacío
                numero_hoja = int(contenido) 
            else:
                numero_hoja = 0
            file.close()
    except FileNotFoundError:
        numero_hoja = 0

    nombre_carpeta_hoja = f"Hoja-{numero_hoja}"
    
    return numero_hoja, nombre_carpeta_hoja

#Funcion para crear carpetas y archivos que almacenan los datos de un cultivo nuevo 
def crear_cultivo():
    
    numero_cultivo, _  = numero_nombre_cultivo()
    
    numero_cultivo += 1 # Aumentar el numero de cultivo para el proximo llamado

    carpeta_cultivo = f"Escaner/Cultivo-{numero_cultivo}"
    
    try:
        os.mkdir(carpeta_cultivo)
        print(f"Carpeta '{carpeta_cultivo}' creada exitosamente.")

        # Crear subcarpetas dentro de la carpeta de cultivo
        subcarpetas = ["Hojas_Escaneo", "Hojas_Area"]
        for subcarpeta in subcarpetas:
            os.mkdir(os.path.join(carpeta_cultivo, subcarpeta))
            print(f"Subcarpetas '{subcarpeta}' creada.")
        

        ##numero_hoja = int(1)  # Reiniciar número de hoja

        # Crear archivos de texto dentro de la carpeta de cultivo
       
        with open(os.path.join("contador.txt"), "w") as file:
            file.write(str(numero_cultivo))
            file.close()
        with open(os.path.join(carpeta_cultivo, "Contador_hojas.txt"), "w") as file:
            file.write(str(""))
            file.close()
        with open(os.path.join(carpeta_cultivo, "Area_hojas.txt"), "w") as file:
            file.write("")  # Puedes añadir contenido si es necesario
            file.close()
        with open(os.path.join(carpeta_cultivo, "Indice_Area_Foliar.txt"), "w") as file:
            file.write("")  # Puedes añadir contenido si es necesario
            file.close()
           
       
    except OSError:
        print("No se pudo crear la estructura de carpetas y archivos para el cultivo.")

#Funcion para crear carpetas que almacenan los datos de una hoja nueva 
def crear_carpeta_hoja():
    
    _ , nombre_cultivo_actual = numero_nombre_cultivo()
    r_cultivo = "Escaner/"+nombre_cultivo_actual
    
    numero_hoja, _ = numero_nombre_hoja(r_cultivo)
    numero_hoja += 1
    carpeta_hoja= f"Hoja-{numero_hoja}"

    try:
        
        subcarpetas = ["Hojas_Escaneo", "Hojas_Area"]

        if os.path.exists(r_cultivo):
            for subcarpeta in subcarpetas:
                ruta_subcarpeta = os.path.join(r_cultivo, subcarpeta)
                os.mkdir(os.path.join(ruta_subcarpeta, carpeta_hoja))
                print(f"Carpeta '{carpeta_hoja}' creada en '{ruta_subcarpeta}'.")
            
            with open(r_cultivo  + "/Contador_hojas.txt", "w") as file:
                file.write(str(numero_hoja))
                file.close()
        else:
            print("La carpeta de cultivo no existe.")
    except OSError:
        print("No se pudo crear la carpeta 'Hoja'.")
