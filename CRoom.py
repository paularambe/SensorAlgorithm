from machine import ADC, Pin
from CSensor import CSensor

class CRoom():
    def __init__(self, nombre, hasWindow):
        self.name=nombre
        self.temperature=0
        self.hasWindow=hasWindow
        self.isWindowOpened=0
        self.isDoorOpened=0
        self.isLightOn=0
        self.sensorList=[]
        self.nSensors=0


    def add_sensor(self, name, pin):
        self.sensorList.append(CSensor(name, pin))


    def check_light(self):


        # print("Checking for light detectors...")
        isLightDet=0
        for sensor in self.sensorList:
            if sensor.name=="Photoresistor":
                light_level=sensor.get_value()
                print("lght lvl: ", light_level)
                isLightDet=1

        if isLightDet:
            # print("Light detector found!")
            if light_level >=1800:
                light=1
            else:
                light=0
            return light
        else:
            print("Sorry! Unable to find a light detector")
            return -1
        
        