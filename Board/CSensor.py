from machine import ADC, Pin

# Configurar el pin GPIO21 como entrada

# Bucle para leer continuamente el estado del pin

class CSensor():
    def __init__(self, nombre,pin):

        self.name=nombre

        if nombre == "Photoresistor":
            self.sensor=ADC(Pin(pin))
        elif nombre == "Movement":
            self.sensor = Pin(21, Pin.IN)

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
        if self.name=="Movement":
            self.rawVal = self.sensor.value()  # Leer el valor digital del pin (0 o 1)
        return self.rawVal
    
    def get_json(self):
        json = {
            "name": self.name,
            "pin": self.pin
        }
        return json
