# EscanerFoliar
Códigos del sistema del dispositivo de escáner foliar para estimar el índice área foliar de cultivos de maíz
  
  El módulo "Princial.py" contiene el programa principal del sistema, se definen las entras y salidas periféricas y las opciones del escáner. 
  
  El módulo "EstrcuturaArchivos" contine las funciones para crear las carpetas y archivos de los cultivos y sus hojas respectivas
  
  El módulo "Area" contiene las funciones para calcular el área de las hojas y guardar sus resultados 
  
  El módulo "IAF" contiene las funciones para calcular el índice de área foliar de un cultivo y guardar sus resultados 
  
  El módulo "RecibirTransferirDatos" contiene las funciones para recibir y transferir los datos desde la tarjeta de almacenamiento SD
  
  El módulo "LCD" contiene las funciones para escribir en la pantalla LCD mediante el protocolo de comunicación I2C

Nota: Los códigos están escritos para ejecutarse en un RaspberryPi, en el programa "Principal.py" se muestran las librerias necesarias a instalarse en la raspberry. 
