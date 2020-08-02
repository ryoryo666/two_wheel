class VW():
    def __init__(self,Sub_data,D,V_slow):
        self.r=Sub_data.R
        self.dir=Sub_data.d
        self.d=D
        self.v_slow=V_slow
        self.v_fast=self.v_slow*((self.r+self.d)/(self.r-self.d))

    def V(self):
        return (self.v_slow+self.v_fast)/2

    def W(self):
        if self.dir=="r":
            return (self.v_slow-self.v_fast)/(2*self.d)
        elif self.dir=="l":
            return (self.v_fast-self.v_slow)/(2*self.d)
