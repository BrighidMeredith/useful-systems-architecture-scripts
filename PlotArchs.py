# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:07:40 2017

Author: Brighid Meredith
Team 13

Purpose: Plot Architectures
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
import scipy.io

from syseng5400.systems_architecture import Metrics as metrics

# Due to the size of the architecture space, not all architectures can be considered at once
# Load a subset, calculate and store the metrics along with features of interest and store

decision_key = pickle.load(open('decision_key.pkl', 'rb'))
archs_dir = [name for name in os.listdir('archs/')]

if 1 == 0:
    d0d0 = pickle.load(open('archs/d1d1.pkl', 'rb'))
    print(len(d0d0))

    #path, dirs, files = os.walk("/archs").__next__()
    #file_count = len(files)
    #print(file_count)
    print (len(archs_dir))

    # 5040 architectures per file
    # 7905 files of architectures
    rows = len(d0d0) * len(archs_dir)
    to_plot = np.zeros((rows,3), dtype = np.int32)
    m = metrics.Metrics()
    row = 0
    for fname in archs_dir:
        with open('archs/'+fname,'rb') as archs_file:
            archs = pickle.load(archs_file)

            for arch in archs:
                cost = m.get_cost(arch)
                reliability = m.get_reliability(arch)
                feature = 0
                to_plot[row][0] = feature
                to_plot[row][1] = cost * 100
                to_plot[row][2] = reliability

                #print(to_plot[row])

    pickle.dump(to_plot,open('metrics_no_features.pkl','wb'))

data = pickle.load(open('metrics_no_features.pkl','rb'))

