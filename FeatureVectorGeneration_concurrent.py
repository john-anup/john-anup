# awg proto FeatureVectorGeneration_concurrent.py
# parallel implementation of MainProg

import numpy as np
import Point as pt
import BinaryMask as mc
import MaskFactory as mf
import MaskPreProcessor as pp
import FileterBank as fb
import pandas as pd
from multiprocessing.dummy import Pool as pl
from multiprocessing.dummy import Lock as lk


def init(loc):
    global lock
    lock = loc


def worker(mask):
    (projections, size) = pp.MaskPreProcessor.project(mask)
    (conv3_result, size) = pp.MaskPreProcessor.conv_3d_4(projections, size, fb.FeatureKernel_4x4x3)
    (max_pool_res, size) = pp.MaskPreProcessor.max_pool(conv3_result, size)
    
    (conv_result, size) = pp.MaskPreProcessor.conv_5(max_pool_res, size, fb.GaussianKernel_5x5)
    (max_pool_res, size) = pp.MaskPreProcessor.max_pool(conv_result, size)
    (hog, size) = pp.MaskPreProcessor.hog(max_pool_res, size)
    feature_vector = np.zeros((1, 181), dtype=float)
    feature_vector[0:1, :][:,-1] = 999999999
    feature_vector[0][0:180] = hog
    lock.acquire()
    pd.DataFrame(feature_vector).to_csv("result.csv", mode='a', header=None, index=False)
    lock.release()


loc = lk()
mask_factory = mf.MaskFactory(".\MaskParameters.csv")
masks = mask_factory.getNext()
while masks != None:
    pool = pl(processes=6,initializer=init, initargs=(loc,))
    pool.map(worker, masks)
    pool.close()
    pool.join()

    masks = mask_factory.getNext()
