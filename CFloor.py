from CRoom import CRoom


class CFloor():
    def __init__(self, num):
        self.num=num
        self.nRooms=0
        self.roomList=[]

    def add_room(self, nombre, hasWindow):
        room=CRoom(nombre, hasWindow)
        self.roomList.append(room)
        self.nRooms=self.nRooms+1
