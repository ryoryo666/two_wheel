import math

class target_getter():
    def __init__(self, t_radius,  direction, t_speed, w_radius, w_separation):
        self.T_radius = t_radius            # Turning Radius
        self.T_speed = t_speed              # Transration Speed
        self.W_radius = w_radius            # Wheel Radius
        self.W_separation = w_separation    # Wheel Separation
        self.Direction=direction            # Turning Direction ("r"" or "l")

        self.Vr=self.T_speed*((self.T_radius+self.W_separation)/self.T_radius)
        self.Vl=self.T_speed*((self.T_radius-self.W_separation)/self.T_radius)
        self.Vr_rpm=(60*self.Vr)/(math.pi*2*self.W_radius)
        self.Vl_rpm=(60*self.Vl)/(math.pi*2*self.W_radius)

    def VR_RPM(self):
        if self.Direction=="r":
            return self.Vl_rpm
        elif self.Direction=="l":
            return self.Vr_rpm

    def VL_RPM(self):
        if self.Direction=="r":
            return self.Vr_rpm
        elif self.Direction=="l":
            return self.Vl_rpm
