from CFloor import CFloor


class CHouse():
    def __init__(self, nombre, nFloors):
        self.name=nombre
        self.nFloors=nFloors
        self.floorList=[]


    def add_floor(self, num):
        floor=CFloor(num)
        self.floorList.append(floor)
        self.nFloors=self.nFloors+1
