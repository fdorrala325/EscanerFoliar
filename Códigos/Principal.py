# Importacion de librerias utilizadas en el programa principal y los secundarios 
import shutil ## sudo pip install pytest-shutil
import subprocess
from gpiozero import Button, OutputDevice  ## sudo pip install gpiozero
from datetime import datetime
from RPi_GPIO_i2c_LCD import lcd ## sudo pip install RPi-GPIO-I2C-LCD
import os ## sudo import os
import cv2 ## sudo pip install opencv-python
import numpy as np
from time import sleep

#Importación de programas secundarios
from RecibirTransferirDatos import *
from EstructuraArchivos import *
from Area import *
from IAF import *
from LCD import *

#Asignaciones de pines GPIO a las entradas y salidas perifericas 
pin_boton_cultivo = 17  #17
pin_boton_hoja = 27  #27
pin_boton_guardar = 23
pin_boton_transferir = 22
rele = OutputDevice(24)

#Botonoes establecidos en resistencia Pull-Down
boton_cultivo = Button(pin_boton_cultivo, pull_up=False)
boton_hoja = Button(pin_boton_hoja, pull_up=False)
boton_guardar = Button(pin_boton_guardar, pull_up=False)
boton_transferir= Button(pin_boton_transferir, pull_up=False)

#Variables para validar que los botones no esten presionados
boton_cultivo_presionado = False
boton_hoja_presionado = False
boton_guardar_presionado = False
boton_transferir_presionado = False

#DPI por defecto del escaner 
dpi = 300

#Programa Principal 
try:
    print("Esperando a que se presione un botón...")
    mostrar_lcd("Bienvenido","Esc. Foliar")

    while True:
        # Creación de cultivo
        if boton_cultivo.is_pressed and not boton_cultivo_presionado:
            crear_cultivo()
            numeroCultivo_actual, _ = numero_nombre_cultivo()
            n_cultivo = f'Cultivo {numeroCultivo_actual}'
            mostrar_lcd(n_cultivo,"Creado")
            boton_cultivo_presionado = True
            sleep(0.5)
        elif not boton_cultivo.is_pressed:
            boton_cultivo_presionado = False
        
        # Creación de hojas
        if boton_hoja.is_pressed and not boton_hoja_presionado:
            crear_carpeta_hoja()
            numeroCultivo_actual ,nombreCultivo_actual = numero_nombre_cultivo()
            numeroHoja_actual, _ = numero_nombre_hoja("Escaner/"+nombreCultivo_actual)
            n_hoja = f'C{numeroCultivo_actual} Hoja {numeroHoja_actual}'
            mostrar_lcd(n_hoja,"Creada")
            boton_hoja_presionado = True
            sleep(0.5)
        elif not boton_hoja.is_pressed:
            boton_hoja_presionado = False

        
        # Guardar y calcular el area de las hojas-IAF de un cultivo 
        # A partir de la imagen almacenada en el escaner luego del proceso de escaneo 
        if boton_guardar.is_pressed and not boton_guardar_presionado:
              
            mostrar_lcd("Procesando")
            
            # Extraer los datos del nombre y numero del cltivo y la hoja actual del sistema
            numeroCultivo_actual ,nombreCultivo_actual = numero_nombre_cultivo()
            numeroHoja_actual ,nombreHoja_actual = numero_nombre_hoja("Escaner/"+nombreCultivo_actual)

            archivo_hoja = 'Area_hojas.txt'
            archivo_IAF = 'Indice_Area_Foliar.txt'
            
            # Proceso para extraer la imagen de la tarjeta SD
            ruta_hojas = "Escaner/"+nombreCultivo_actual + '/Hojas_Escaneo/' + nombreHoja_actual
                              
            nombre_archivo_hoja = f'Hoja_{numeroHoja_actual:04}.jpg'
            nombre_archivo_hojaArea = f'Hoja_{numeroHoja_actual:04}_Area.jpg' 
            
            #Activar el relé para poner el escáner en modo transferencia de datos 
            rele.on()
            sleep(3)
            recibir_datos(ruta_hojas, nombre_archivo_hoja)
            sleep(0.5)
            
            # Desactivar el relé para dejar el escáner en modo escaneo 
            rele.off()
                                  
            # Establecimiento de rutas para guardar imagenes, área e IAF
            ruta_imagen = ruta_hojas + '/' + nombre_archivo_hoja
            ruta_ImagenArea = "Escaner/" + nombreCultivo_actual + "/Hojas_Area/" + nombreHoja_actual + "/" + nombre_archivo_hojaArea
            ruta_areaTXT = "Escaner/" + nombreCultivo_actual + "/Area_hojas.txt"
            ruta_IAFTXT = "Escaner/" + nombreCultivo_actual + '/Indice_Area_Foliar.txt'
            
            # Calcular y guardar el área de la hoja 
            area_hoja = area_foliar(ruta_imagen, dpi, ruta_ImagenArea)
            guardar_Area(area_hoja, numeroHoja_actual, ruta_areaTXT)

            # Calcular y guardar el índice de área foliar             
            indice_area_foliar = calcularIAF(ruta_areaTXT)
            guardar_IAF(indice_area_foliar, numeroCultivo_actual, ruta_IAFTXT)
            sleep(0.2)
            
            # Mostrar en LCD los resultados 
            Dato1 = f'A = {area_hoja} cm2'
            Dato2 = f'IAF = {indice_area_foliar}'
            
            mostrar_lcd(Dato1, Dato2)
            
            print(area_hoja)# LCD
            print(indice_area_foliar)
            boton_guardar_presionado = True
            sleep(0.5)
        elif not boton_guardar.is_pressed:
           boton_guardar_presionado = False
        
        # Transferir los archivos de los Cultivos de la raspberry a la SD
        if boton_transferir.is_pressed and not boton_transferir_presionado:
            mostrar_lcd("Transfer.", "Datos")

            #Activar el relé para poner el escáner en modo transferencia de datos 
            rele.on()
            sleep(3)

            # Establecimiento de rutas para guardar los archivos en de la raspberry a la SD
            ruta_origen_rasp = "/home/Daniel/Escaner"
            ruta_destino_sd = "/media/Daniel/disk/DCIM/ESCANER"
            
            transferir_datos(ruta_origen_rasp, ruta_destino_sd)

            sleep(0.5)

            # Desactivar el relé para dejar el escáner en modo escaneo 
            rele.off()
            boton_transferir_presionado = True
            sleep(0.5)
        elif not boton_transferir.is_pressed:
            boton_guardar_presionado = False

except KeyboardInterrupt:
    print("Programa finalizado.")

