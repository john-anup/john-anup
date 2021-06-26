# awg proto MaskPreProcessor.py

import numpy as np
import Point as pt
import BinaryMask
import FileterBank as fb

class MaskPreProcessor:
    "the input to the preprocessor shall be of equal dimension x,y,z"

    @staticmethod
    def project(mask:BinaryMask):
        side_len = int(mask.get_side_len())
        projection = np.zeros((int(3), int(side_len * side_len)), dtype = float)
        for dep in range(0, side_len):
            slice = mask.get_slice(dep)
            for row in range(0, side_len):
                for col in range(0, side_len):
                    value = slice[row*side_len + col]
                    projection[0][row * side_len + dep] += value #left right
                    projection[1][col * side_len + dep] += value #top bottom
                    projection[2][row * side_len + col] += value #front back

        #print("Side View: \n", projection[0])
        #print("Top View: \n", projection[1])
        #print("Front View: \n", projection[2])

        return (projection, side_len)


    @staticmethod
    def max_pool(input, in_side_len):
        side_len = int(float(in_side_len) / 2.0 + 0.5)
        maxPoolRes = np.zeros((side_len*side_len), dtype = float)
        for row in range(0, side_len):
            for col in range(0, side_len):
                row_t = min(row*2, in_side_len - 1)
                row_b = min(row*2 + 1, in_side_len - 1)
                col_l = min(col*2, in_side_len - 1)
                col_r = min(col*2 + 1, in_side_len - 1)
                maxPoolRes[row*side_len + col] = max(input[row_t * in_side_len + col_l], input[row_t * in_side_len + col_r], input[row_b * in_side_len + col_l], input[row_b  * in_side_len + col_r])
        #print("max pool out: \n", maxPoolRes)

        return (maxPoolRes, side_len)


    @staticmethod
    def conv_3d_4(input, in_side_len, threeDKernel):
        side_len = in_side_len - 3
        threeDConvRes = np.zeros((side_len * side_len), dtype = float)
        for row in range(0, side_len):
            for col in range(0, side_len):
                threeDConvRes[row * side_len + col] = input[0][(row + 0) * in_side_len + col + 0] * threeDKernel[0][0] + input[0][(row + 0) * in_side_len + col + 1] * threeDKernel[0][1] + input[0][(row + 0) * in_side_len + col + 2] * threeDKernel[0][2] + input[0][(row + 0) * in_side_len + col + 3] * threeDKernel[0][3] + input[0][(row + 1) * in_side_len + col + 0] * threeDKernel[0][4] + input[0][(row + 1) * in_side_len + col + 1] * threeDKernel[0][5] + input[0][(row + 1) * in_side_len + col + 2] * threeDKernel[0][6] + input[0][(row + 1) * in_side_len + col + 3] * threeDKernel[0][7] + input[0][(row + 2) * in_side_len + col + 0] * threeDKernel[0][8] + input[0][(row + 2) * in_side_len + col + 1] * threeDKernel[0][9] + input[0][(row + 2) * in_side_len + col + 2] * threeDKernel[0][10] + input[0][(row + 2) * in_side_len + col + 3] * threeDKernel[0][11] + input[0][(row + 3) * in_side_len + col + 0] * threeDKernel[0][12] + input[0][(row + 3) * in_side_len + col + 1] * threeDKernel[0][13] + input[0][(row + 3) * in_side_len + col + 2] * threeDKernel[0][14] + input[0][(row + 3) * in_side_len + col + 3] * threeDKernel[0][15] + input[1][(row + 0) * in_side_len + col + 0] * threeDKernel[1][0] + input[1][(row + 0) * in_side_len + col + 1] * threeDKernel[1][1] + input[1][(row + 0) * in_side_len + col + 2] * threeDKernel[1][2] + input[1][(row + 0) * in_side_len + col + 3] * threeDKernel[1][3] + input[1][(row + 1) * in_side_len + col + 0] * threeDKernel[1][4] + input[1][(row + 1) * in_side_len + col + 1] * threeDKernel[1][5] + input[1][(row + 1) * in_side_len + col + 2] * threeDKernel[1][6] + input[1][(row + 1) * in_side_len + col + 3] * threeDKernel[1][7] + input[1][(row + 2) * in_side_len + col + 0] * threeDKernel[1][8] + input[1][(row + 2) * in_side_len + col + 1] * threeDKernel[1][9] + input[1][(row + 2) * in_side_len + col + 2] * threeDKernel[1][10] + input[1][(row + 2) * in_side_len + col + 3] * threeDKernel[1][11] + input[1][(row + 3) * in_side_len + col + 0] * threeDKernel[1][12] + input[1][(row + 3) * in_side_len + col + 1] * threeDKernel[1][13] + input[1][(row + 3) * in_side_len + col + 2] * threeDKernel[1][14] + input[1][(row + 3) * in_side_len + col + 3] * threeDKernel[1][15] + input[2][(row + 0) * in_side_len + col + 0] * threeDKernel[2][0] + input[2][(row + 0) * in_side_len + col + 1] * threeDKernel[2][1] + input[2][(row + 0) * in_side_len + col + 2] * threeDKernel[2][2] + input[2][(row + 0) * in_side_len + col + 3] * threeDKernel[2][3] + input[2][(row + 1) * in_side_len + col + 0] * threeDKernel[2][4] + input[2][(row + 1) * in_side_len + col + 1] * threeDKernel[2][5] + input[2][(row + 1) * in_side_len + col + 2] * threeDKernel[2][6] + input[2][(row + 1) * in_side_len + col + 3] * threeDKernel[2][7] + input[2][(row + 2) * in_side_len + col + 0] * threeDKernel[2][8] + input[2][(row + 2) * in_side_len + col + 1] * threeDKernel[2][9] + input[2][(row + 2) * in_side_len + col + 2] * threeDKernel[2][10] + input[2][(row + 2) * in_side_len + col + 3] * threeDKernel[2][11] + input[2][(row + 3) * in_side_len + col + 0] * threeDKernel[2][12] + input[2][(row + 3) * in_side_len + col + 1] * threeDKernel[2][13] + input[2][(row + 3) * in_side_len + col + 2] * threeDKernel[2][14] + input[2][(row + 3) * in_side_len + col + 3] * threeDKernel[2][15]
                
        #print("3D Convolved out: \n", threeDConvRes)

        return (threeDConvRes, side_len)


    @staticmethod
    def conv_5(input, in_side_len, kernel):
        side_len = in_side_len - 4
        convRes = np.zeros((side_len * side_len), dtype = float)
        for row in range(0, side_len):
            for col in range(0, side_len):
                convRes[row * side_len + col] = input[(row + 0) * in_side_len + col + 0] * kernel[0] + input[(row + 0) * in_side_len + col + 1] * kernel[1] + input[(row + 0) * in_side_len + col + 2] * kernel[2] + input[(row + 0) * in_side_len + col + 3] * kernel[3] + input[(row + 0) * in_side_len + col + 4] * kernel[4] + input[(row + 1) * in_side_len + col + 0] * kernel[5] + input[(row + 1) * in_side_len + col + 1] * kernel[6] + input[(row + 1) * in_side_len + col + 2] * kernel[7] + input[(row + 1) * in_side_len + col + 3] * kernel[8] + input[(row + 1) * in_side_len + col + 4] * kernel[9] + input[(row + 2) * in_side_len + col + 0] * kernel[10] + input[(row + 2) * in_side_len + col + 1] * kernel[11] + input[(row + 2) * in_side_len + col + 2] * kernel[12] + input[(row + 2) * in_side_len + col + 3] * kernel[13] + input[(row + 2) * in_side_len + col + 4] * kernel[14] + input[(row + 3) * in_side_len + col + 0] * kernel[15] + input[(row + 3) * in_side_len + col + 1] * kernel[16] + input[(row + 3) * in_side_len + col + 2] * kernel[17] + input[(row + 3) * in_side_len + col + 3] * kernel[18] +input[(row + 3) * in_side_len + col + 4] * kernel[19] +input[(row + 4) * in_side_len + col + 0] * kernel[20] + input[(row + 4) * in_side_len + col + 1] * kernel[21] + input[(row + 4) * in_side_len + col + 2] * kernel[22] + input[(row + 4) * in_side_len + col + 3] * kernel[23] +input[(row + 4) * in_side_len + col + 4] * kernel[24]
                
        #print("Convolved 5 out: \n", convRes)

        return (convRes, side_len)


    @staticmethod
    def conv_4(input, in_side_len, kernel):
        side_len = in_side_len - 3
        convRes = np.zeros((side_len * side_len), dtype = float)
        for row in range(0, side_len):
            for col in range(0, side_len):
                convRes[row * side_len + col] = input[(row + 0) * in_side_len + col + 0] * kernel[0] + input[(row + 0) * in_side_len + col + 1] * kernel[1] + input[(row + 0) * in_side_len + col + 2] * kernel[2] + input[(row + 0) * in_side_len + col + 3] * kernel[3] + input[(row + 1) * in_side_len + col + 0] * kernel[4] + input[(row + 1) * in_side_len + col + 1] * kernel[5] + input[(row + 1) * in_side_len + col + 2] * kernel[6] + input[(row + 1) * in_side_len + col + 3] * kernel[7] + input[(row + 2) * in_side_len + col + 0] * kernel[8] + input[(row + 2) * in_side_len + col + 1] * kernel[9] + input[(row + 2) * in_side_len + col + 2] * kernel[10] + input[(row + 2) * in_side_len + col + 3] * kernel[11] + input[(row + 3) * in_side_len + col + 0] * kernel[12] + input[(row + 3) * in_side_len + col + 1] * kernel[13] + input[(row + 3) * in_side_len + col + 2] * kernel[14] + input[(row + 3) * in_side_len + col + 3] * kernel[15]
                
        #print("Convolved out: \n", convRes)

        return (convRes, side_len)


    @staticmethod
    def conv_3(input, in_side_len, kernel):
        side_len = in_side_len - 2
        convRes = np.zeros((side_len * side_len), dtype = float)
        for row in range(0, side_len):
            for col in range(0, side_len):
                convRes[row * side_len + col] = input[(row + 0) * in_side_len + col + 0] * kernel[0] + input[(row + 0) * in_side_len + col + 1] * kernel[1] + input[(row + 0) * in_side_len + col + 2] * kernel[2] + input[(row + 1) * in_side_len + col + 0] * kernel[3] + input[(row + 1) * in_side_len + col + 1] * kernel[4] + input[(row + 1) * in_side_len + col + 2] * kernel[5] + input[(row + 2) * in_side_len + col + 0] * kernel[6] + input[(row + 2) * in_side_len + col + 1] * kernel[7] + input[(row + 2) * in_side_len + col + 2] * kernel[8]
                
        #print("Convolved 3 out: \n", convRes)

        return (convRes, side_len)


    @staticmethod
    def hog(input, in_side_len):
        (grad_x, side_len_x) = MaskPreProcessor.conv_3(input, in_side_len, fb.Sobel_x_3x3)
        (grad_y, side_len_y) = MaskPreProcessor.conv_3(input, in_side_len, fb.Sobel_y_3x3)
        magnitude = np.sqrt(np.square(grad_x) + np.square(grad_y))
        direction = np.divide(np.arctan2(grad_y, grad_x), 2.0)

        histogram_of_gradiants = np.zeros(180)

        for row in range(0, side_len_y):
            for col in range(0, side_len_x):
                dir_deg = int((direction[row*side_len_x + col] + 1.570796326795) * 57.295779513082 + 0.5)
                dir_deg = min(dir_deg, 179)
                dir_deg = max(dir_deg, 0)
                histogram_of_gradiants[dir_deg] += magnitude[row*side_len_x + col]

        #print("HOG out: \n", histogram_of_gradiants)
        return (histogram_of_gradiants, 180)




# Appendix 1
# here we assume that x=y so size of combined proj = y(2z+y)
# self.__combinedProj = np.zeros(self.__inputDim.y * (2 * self.__inputDim.z + self.__inputDim.y))
# self.__combinedProj[row * (2*self.__inputDim.z + self.__inputDim.y) + 3*dep] += value
# self.__combinedProj[col * (2*self.__inputDim.z + self.__inputDim.y) + 3*dep+1] += value
# self.__combinedProj[row * (2*self.__inputDim.z + self.__inputDim.y) + 3*col+2] += value
# print("Combined View: \n", self.__combinedProj)