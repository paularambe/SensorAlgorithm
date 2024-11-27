from machine import ADC, Pin
import random
# Configurar el pin GPIO21 como entrada

# Bucle para leer continuamente el estado del pin

class CSensor():
    def __init__(self, nombre,pin):

        self.name=nombre

        if nombre == "Photoresistor":
            self.sensor=ADC(Pin(pin))
        elif nombre == "Movement":
            self.sensor = Pin(pin, Pin.IN)
        elif nombre == "Button":
            self.sensor = Pin(pin, Pin.IN, Pin.PULL_UP)


        self.pin=pin
        self.rawVal=0


            
    
    def get_value(self):
        if self.name=="Photoresistor":
            self.sensor.atten(ADC.ATTN_11DB)  # Configura el rango de voltaje (0-3.3V)
            val= self.sensor.read()
            if val >= 1200:
                self.rawVal = 1
            else:
                self.rawVal = 0
        elif self.name=="Movement":
            self.rawVal = self.sensor.value()  # Leer el valor digital del pin (0 o 1)
            
        elif self.name == "Button":
            if self.sensor.value()==1:
                self.rawVal = 0
            else:
                self.rawVal = 1
            
        return self.rawVal
    
    def get_json(self):
        json = {
            "name": self.name,
            "pin": self.pin
        }
        return json
