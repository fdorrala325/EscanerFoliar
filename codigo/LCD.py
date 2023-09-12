from RPi_GPIO_i2c_LCD import lcd  # pip install RPi-GPIO-I2C-LCD
from time import sleep

## Dirección I2C
i2c_address = 0x27

## Inicializar LCD
lcdDisplay = lcd.HD44780(i2c_address)

#Función para escribir en la LCD

def mostrar_lcd(Dato1=None, Dato2=None):
	
	lcdDisplay.clear()
	
	# Establece un valor predeterminado para línea 2 si no se proporciona
	if Dato1 is None:
		Dato1 = ""
	
	# Establece un valor predeterminado para línea 1 si no se proporciona
	
	if Dato2 is None:
		Dato2 = ""

	lcdDisplay.set(Dato1,1)
	lcdDisplay.set(Dato2,2)

#Función para lipiar caracteres en la LCD

def lcd_clear():
	lcdDisplay.clear()
