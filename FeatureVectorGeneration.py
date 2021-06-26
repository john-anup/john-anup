# awg proto FeatureVectorGeneration.py

# if the input data is of size 256, then we will endup with feature vector of 900. one option is to perform max pooling before we start 3D convolution
# 3D convolution is based on shape, next convolution layer is based on edges, the final one is based on, thinking if Gaussian is a good idea?
# Do we have to use Relu? it looks like we will lose ever more information

import numpy as np
import Point as pt
import BinaryMask as mc
import MaskFactory as mf
import MaskPreProcessor as pp
import FileterBank as fb
import pandas as pd

feature_vector = np.zeros((3072, 181), dtype=float)
feature_vector[0:1024, :][:,-1] = 0 # -> DICE / Jacard -> large objects
feature_vector[1024:2048, :][:,-1] = 1 # -> HD -> shape is important / several small objects
feature_vector[2048:3072, :][:,-1] = 2 # -> MHD -> general shape and alignment -> holes less dense objects.

ctr = 0
mask_factory = mf.MaskFactory(".\MaskParameters.csv")
masks = mask_factory.getNext()
while masks != None:
    for mask in masks:
        #mask.dump("C:\\temp\\mask{}.raw".format(ctr))

        (projections, size) = pp.MaskPreProcessor.project(mask)

        (conv3_result, size) = pp.MaskPreProcessor.conv_3d_4(projections, size, fb.FeatureKernel_4x4x3)
        (max_pool_res, size) = pp.MaskPreProcessor.max_pool(conv3_result, size)

        (conv_result, size) = pp.MaskPreProcessor.conv_5(max_pool_res, size, fb.GaussianKernel_5x5)
        (max_pool_res, size) = pp.MaskPreProcessor.max_pool(conv_result, size)

        (hog, size) = pp.MaskPreProcessor.hog(max_pool_res, size)
        feature_vector[ctr][0:180] = hog
        ctr = ctr + 1
        print(ctr)

    masks = mask_factory.getNext()

print(feature_vector)
pd.DataFrame(feature_vector).to_csv("result.csv", header=None, index=False)
