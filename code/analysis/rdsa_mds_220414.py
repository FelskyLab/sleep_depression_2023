import pandas as pd
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import sklearn
from sklearn import manifold


aggregated_results = np.load('rdsa_lower_triangle_all_rois.npy')
mds = manifold.MDS(
    n_components=2,
    max_iter=400,
    eps=1e-9,
    random_state=42,
    dissimilarity="euclidean",
    n_jobs=8,
)

npos = mds.fit_transform(aggregated_results)
npos *= np.sqrt((aggregated_results ** 2).sum()) / np.sqrt((npos ** 2).sum())

np.save('mds_results_allrois_220414.npy', npos)
