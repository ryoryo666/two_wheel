import math

class DXY():
    def __init__(self,V,A):
        self.v=V
        self.a=A

    def dx(self):
        return self.v*math.cos(self.a)

    def dy(self):
        return self.v*math.sin(self.a)
