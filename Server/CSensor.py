
# Configurar el pin GPIO21 como entrada

# Bucle para leer continuamente el estado del pin

class CSensor():
    def __init__(self, nombre,pin):

        self.name=nombre

        if nombre == "Photoresistor":
            self.sensor=0
        elif nombre == "Movement":
            self.sensor = 21

        self.pin=pin
        self.rawVal=0
    
    def get_json(self):
        json = {
            "name": self.name,
            "pin": self.pin
        }
        return json
