class CESP32():
    def __init__(self, name, IP , PORT, remoteADD,SENSORS):
        self.name=name
        self.IP=IP
        self.PORT=PORT
        self.remoteADD=remoteADD
        self.sensors=SENSORS
        self.isBoardCon=0

