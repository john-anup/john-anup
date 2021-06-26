# awg proto MaskFactory.py
import Point as pt
import BinaryMask as mc
import MaskTransform as mt

class MaskFactory:
    "class that creates mask objects based on input text file"

    def __init__(self, path):
        self.__file = open(path, 'r')
        print(self.__file.readline())

    def getNext(self):
        line = self.__file.readline()
        
        if len(line) < 5:
            return None
        else:
            #Data Augmentation = 26
            line = line + ";shea,0.1,0.0,0.0;shea,0.0,0.1,0.0;shea,0.0,0.0,0.1;shea,0.1,0.1,0.0;shea,0.0,0.1,0.1;shea,0.1,0.0,0.1;shea,0.1,0.1,0.1;shea,0.2,0.0,0.0;shea,0.0,0.2,0.0;shea,0.0,0.0,0.2;shea,0.2,0.2,0.0;shea,0.0,0.2,0.2;shea,0.2,0.0,0.2;shea,0.2,0.2,0.2;shea,0.1,0.1,0.2;shea,0.2,0.1,0.1;shea,0.1,0.2,0.1;shea,0.2,0.2,0.1;shea,0.1,0.2,0.2;shea,0.2,0.1,0.2;shea,0.2,0.1,0.0;shea,0.2,0.0,0.1;shea,0.1,0.2,0.0;shea,0.1,0.0,0.2;shea,0.0,0.1,0.2;shea,0.0,0.2,0.1;"
            mask = mc.BinaryMask(pt.Point3(128,128,128))
            arrayOfMasks = []
            objects = line.split(';')
            
            for object in objects:
                parameters = object.split(',')
                if parameters[0] == "elli":
                    mask.add_ellipsoid(pt.Point3(int(parameters[1]), int(parameters[2]), int(parameters[3])), 
                                       pt.Point3(int(parameters[4]), int(parameters[5]), int(parameters[6])),
                                       int(parameters[7]))
                    print(object)

                elif parameters[0] == "pris":
                    mask.add_prism(int(parameters[1]), 
                                   int(parameters[2]), 
                                   int(parameters[3]), 
                                   pt.Point3(int(parameters[4]), int(parameters[5]), int(parameters[6])),
                                   int(parameters[7]))
                    print(object)

                elif parameters[0] == "cubo":
                    mask.add_cuboid(pt.Point3(int(parameters[1]), int(parameters[2]), int(parameters[3])), 
                                    pt.Point3(int(parameters[4]), int(parameters[5]), int(parameters[6])),
                                    int(parameters[7]))
                    print(object)

                elif parameters[0] == "sphe":
                    mask.add_sphere(float(parameters[1]), 
                                    pt.Point3(int(parameters[2]), int(parameters[3]), int(parameters[4])),
                                    int(parameters[5]))
                    print(object)

                elif parameters[0] == "cyli":
                    mask.add_cylinder(float(parameters[1]), 
                                      int(parameters[2]), 
                                      pt.Point3(int(parameters[3]), int(parameters[4]), int(parameters[5])),
                                      int(parameters[6]))
                    print(object)

                elif parameters[0] == "scal":
                    scaledMask = mt.MaskTransform(pt.Point3(128,128,128))
                    scaledMask.scale(mask, float(parameters[1]), float(parameters[2]), float(parameters[3]))
                    arrayOfMasks.append(scaledMask)
                    print(object)

                elif parameters[0] == "shea":
                    shearedMask = mt.MaskTransform(pt.Point3(128,128,128))
                    shearedMask.shear(mask, float(parameters[1]), float(parameters[2]), float(parameters[3]))
                    arrayOfMasks.append(shearedMask)
                    print(object)

            arrayOfMasks.append(mask)

            return arrayOfMasks
