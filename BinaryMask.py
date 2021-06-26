# awg proto BinaryMask.py

import numpy as np
import Point as pt

class BinaryMask:
    "class to create different types of masks"

    def __init__ (self, dimension = pt.Point3(10,10,10)):
        self._dim = dimension
        self._mask = np.zeros((int(self._dim.z), int(self._dim.y*self._dim.x)), dtype= np.bool)
        self._center = self._dim.sdivr(2)


    def get_side_len(self):
        return int(self._dim.x)


    def get_slice(self, dep):
        return self._mask[dep]


    def __setSliceMask(self, halfLength, off_center_z, white, frame):
        for dep in range(
                max(0, int(off_center_z-halfLength)),
                min(int(self._dim.z), int(off_center_z+halfLength))):
            if white == True:
                self._mask[dep]=np.logical_or(self._mask[dep] , frame)
            else:
                self._mask[dep]=np.multiply(self._mask[dep] , frame)


    def add_cuboid ( self, dim:pt.Point3, offset = pt.Point3(0,0,0), white = True) :
        off_center = self._center.subr(offset)
        frame = np.zeros(int(self._dim.x*self._dim.y), dtype= np.bool)
        if white == False:
            frame = np.ones(int(self._dim.x*self._dim.y), dtype= np.bool)
        startr = int(max(off_center.y - dim.y / 2, 0))
        stopr = int(min(off_center.y + dim.y /2, self._dim.y))
        startc = int(max(off_center.x - dim.x / 2, 0))
        stopc = int(min(off_center.x + dim.x /2, self._dim.x))
        for row in range(startr, stopr):
            for col in range(startc, stopc):
                frame[row*int(self._dim.x)+col] = white
        
        BinaryMask.__setSliceMask(self, dim.z/2, off_center.z, white, frame)


    # if abc.x,y,z are equal -> sphere. if abc has 2 parameters equal -> spheroid
    def add_ellipsoid ( self, abc:pt.Point3, offset = pt.Point3(0,0,0), white = True) :
        off_center = self._center.subr(offset)
        for dep in range(0, int(self._dim.z)):
            for row in range(0, int(self._dim.y)):
                for col in range(0, int(self._dim.x)):
                    if (pow((col-off_center.x)/abc.x, 2.0) + 
                    pow((row-off_center.y)/abc.y, 2.0) + 
                    pow((dep-off_center.z)/abc.z, 2.0)) < 1.0 :
                        val = self._mask[dep][row*int(self._dim.x)+col]
                        self._mask[dep][row*int(self._dim.x)+col] = white
                        #print(col, row, dep)
    
    
    def add_sphere ( self, radius, offset= pt.Point3(0,0,0), white = True) :
        BinaryMask.add_ellipsoid(self, pt.Point3(radius, radius, radius), offset, white)

    
    def add_cylinder(self, radius, length, offset = pt.Point3(0,0,0), white = True) :
        off_center = self._center.subr(offset)
        frame = np.zeros(int(self._dim.x*self._dim.y), dtype= np.bool)
        if white == False:
            frame = np.ones(int(self._dim.x*self._dim.y), dtype= np.bool)
        for row in range(0, int(self._dim.y)):
            for col in range(0, int(self._dim.x)):
                if np.sqrt(
                        pow(col-off_center.x, 2.0) + 
                        pow(row-off_center.y, 2.0)) < radius :
                    frame[row*int(self._dim.x)+col] = white
                    
        BinaryMask.__setSliceMask(self, length/2, off_center.z, white, frame)


    def __tg_area(self, p1, p2, p3):
        return abs((p1.x * (p2.y - p3.y) + 
                    p2.x * (p3.y - p1.y) + 
                    p3.x * (p1.y - p2.y)) / 2.0)

    def __tg_isinside(self, p1, p2, p3, p):
        A = self.__tg_area(p1, p2, p3)
        A1 = self.__tg_area(p, p2, p3)
        A2 = self.__tg_area (p1, p, p3)
        A3 = self.__tg_area (p1, p2, p)
        if abs(A - (A1 + A2 + A3)) < 0.0001 :
            return True
        else:
            return False

    def add_prism(self, base, height, length, offset = pt.Point3(0,0,0), white = True):
        off_center = self._center.subr(offset)
        frame = np.zeros(int(self._dim.x*self._dim.y), dtype= np.bool)
        if white == False:
            frame = np.ones(int(self._dim.x*self._dim.y), dtype= np.bool)
        p1 = pt.Point2(off_center.x, 
                    max(0, off_center.y - height/2.0))
        p2 = pt.Point2(max(0, off_center.x - base/2.0), 
                    min(self._dim.y, off_center.y + height/2.0))
        p3 = pt.Point2(min(self._dim.x, off_center.x + base/2.0), 
                    min(self._dim.y, off_center.y + height/2.0))
        min_row = int(min(p1.y, p2.y, p3.y))
        max_row = int(max(p1.y, p2.y, p3.y))
        min_col = int(min(p1.x, p2.x, p3.x))
        max_col = int(max(p1.x, p2.x, p3.x))
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                if self.__tg_isinside(p1, p2, p3, pt.Point2(col, row)) :
                    frame[row*int(self._dim.x)+col] = white
                    
        BinaryMask.__setSliceMask(self, length/2, off_center.z, white, frame)


    def dump(self, path):
        f=open(path, 'wb')
        for dep in range(0, int(self._dim.z)):
            f.write(self._mask[dep])
