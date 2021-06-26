# awg proto MaskTransform.py

import Point
import BinaryMask as bm

class MaskTransform(bm.BinaryMask):
    
    def shear(self, mask, coeff_x, coeff_y, coeff_z):
        for dep in range(0, int(self._dim.z)):
            for row in range(0, int(self._dim.y)):
                for col in range(0, int(self._dim.x)):
                    col_map = max(int(col + coeff_y*row + coeff_z*dep), 0)
                    col_map = min(col_map, int(self._dim.x -1))
                    row_map = max(int(row + coeff_x*col + coeff_z*dep), 0)
                    row_map = min(row_map, int(self._dim.y -1))
                    dep_map = max(int(dep + coeff_x*col + coeff_y*row), 0)
                    dep_map = min(dep_map, int(self._dim.z -1))
                    self._mask[dep][row*int(self._dim.x)+col] = mask._mask[dep_map][row_map*int(self._dim.x) + col_map]


    def scale(self, mask, fact_x, fact_y, fact_z):
        for dep in range(0, int(self._dim.z)):
            for row in range(0, int(self._dim.y)):
                for col in range(0, int(self._dim.x)):
                    col_map = max(int((col-self._center.x)/fact_x + self._center.x), 0)
                    col_map = min(col_map, int(self._dim.x -1))
                    row_map = max(int((row-self._center.y)/fact_y + self._center.y), 0)
                    row_map = min(row_map, int(self._dim.y -1))
                    dep_map = max(int((dep - self._center.z)/fact_z + self._center.z), 0)
                    dep_map = min(dep_map, int(self._dim.z -1))
                    self._mask[dep][row*int(self._dim.x)+col] = mask._mask[dep_map][row_map*int(self._dim.x) + col_map]