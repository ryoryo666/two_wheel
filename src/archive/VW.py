class VW():
    def __init__(self,Turning_info,d,v_slow):
        self.r=Turning_info.Radius
        self.Direction=Turning_info.Direction
        self.D=d
        self.V_Slow=v_slow
        self.V_Fast=self.V_Slow*((self.r+self.D)/(self.r-self.D))

    def V(self):
        return (self.V_Slow+self.V_Fast)/2

    def W(self):
        if self.Direction=="r":
            return (self.V_Slow-self.V_Fast)/(2*self.D)
        elif self.Direction=="l":
            return (self.V_Fast-self.V_Slow)/(2*self.D)
