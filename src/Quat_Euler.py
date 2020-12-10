import tf

class Quat_TF(object):
    def __init__(self, x,y,z,w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
        self.e = tf.transformations.euler_from_quaternion((self.x, self.y, self.z, self.w))

    def Euler_z(self):
        return self.e[2]
