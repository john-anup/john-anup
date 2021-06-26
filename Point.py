# awg proto Point.py

import copy

class Point2:

    def __init__(self, x, y):
        self.x = x
        self.y = y
           
    def sub(self, val):
        self.x -= val.x
        self.y -= val.y
        
    def add(self, val):
        self.x += val.x
        self.y += val.y


class Point3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def sub(self, val):
        self.x -= val.x
        self.y -= val.y
        self.z -= val.z
        
    def subr(self, val):
        ret_val = copy.deepcopy(self)
        ret_val.sub(val)
        return ret_val
        
    def ssub(self, val):
        self.x -= val
        self.y -= val
        self.z -= val
        
    def add(self, val):
        self.x += val.x
        self.y += val.y
        self.z += val.z
        
    def sadd(self, val):
        self.x += val
        self.y += val
        self.z += val
        
    def sdiv(self, val):
        self.x /= val
        self.y /= val
        self.z /= val
        
    def sdivr(self, val):
        ret_val = copy.deepcopy(self)
        ret_val.sdiv(val)
        return ret_val