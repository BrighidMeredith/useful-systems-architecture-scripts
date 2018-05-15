# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:07:40 2017

Author: Brighid Meredith
Team 13

Purpose: Plot Architectures
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
import random

from syseng5400.systems_architecture import Metrics as metrics

# Due to the size of the architecture space, not all architectures can be considered at once
# Load a subset, calculate and store the metrics along with features of interest and store

decision_key = pickle.load(open('decision_key.pkl', 'rb'))
archs_dir = [name for name in os.listdir('archs/')]
sample_size = 1000000

# Save sample for human viewing (and for teammates still using Matlab)
with open('readable_archs_metrics.txt','w') as fn:
    #fn.write(str(decision_key))
    fn.write("architecture,cost,reliability")
    if 1 == 1:
        d0d0 = pickle.load(open('archs/d0d0.pkl', 'rb'))
        print(len(d0d0))

        # path, dirs, files = os.walk("/archs").__next__()
        # file_count = len(files)
        # print(file_count)
        print(len(archs_dir))

        # 5040 architectures per file
        # 7905 files of architectures
        rows = len(d0d0) * len(archs_dir)
        # Examine each feature from each decision separately
        # Save multiple datasets
        to_plot = np.zeros((rows, 10), dtype=np.int32)  # 2 cols for cost reliability

        m = metrics.Metrics()
        row = 0
        for fname in archs_dir:
            with open('archs/' + fname, 'rb') as archs_file:
                archs = pickle.load(archs_file)

                for arch in archs:
                    if random.random() < .1:
                        cost = m.get_cost(arch)
                        reliability = m.get_reliability(arch)
                        fn.write(str(arch)+",{},{}".format(cost,reliability))
                        row += 1
                if row >= sample_size:
                    break
        pickle.dump(to_plot, open('metrics_all_architectures.pkl', 'wb'))

fn_all_archs_no_features = 'metrics_no_features.pkl'

data = pickle.load((open('metrics_all_architectures.pkl', 'rb')))


if 1 == 0:
    d0d0 = pickle.load(open('archs/d0d0.pkl', 'rb'))
    print(len(d0d0))

    #path, dirs, files = os.walk("/archs").__next__()
    #file_count = len(files)
    #print(file_count)
    print (len(archs_dir))

    # 5040 architectures per file
    # 7905 files of architectures
    rows = len(d0d0) * len(archs_dir)
    # Examine each feature from each decision separately
    # Save multiple datasets
    to_plot = np.zeros((rows,10), dtype = np.int32) # 2 cols for cost reliability


    m = metrics.Metrics()
    row = 0
    for fname in archs_dir:
        with open('archs/'+fname,'rb') as archs_file:
            archs = pickle.load(archs_file)

            for arch in archs:
                cost = m.get_cost(arch)
                reliability = m.get_reliability(arch)
                to_plot[row][0] = cost
                to_plot[row][1] = reliability*100
                # Pull out feature data
                for i, dec in enumerate(arch):
                    if type(dec) != list:
                        feature = dec
                    else:
                        feature = len(dec)
                    to_plot[row][2+i] = feature
                row += 1
    pickle.dump(to_plot,open('metrics_all_architectures.pkl','wb'))

fn_all_archs_no_features = 'metrics_no_features.pkl'

data = pickle.load((open('metrics_all_architectures.pkl','rb')))

print(data.shape)

new_data = np.zeros((sample_size,10), dtype = np.int32)
for i in range(sample_size):
    randrow = random.randint(0,len(data[:,0])-1)
    for j in range(data.shape[1]):
        new_data[i][j] = data[randrow][j]
        #print(data[randrow][j])
#data = [data[random.randint(0,len(data[:,0])-1)] for i in range(10000)]

feature_key =  {1:'payload', 2:'num of platform', 3:'num of launch sites', 4:'num of monitors',
                    5:'sensor type', 6:'type of spacecraft', 7:'orbit', 8:'headquarters type'}

if 1 == 0:

    for i,key in enumerate(feature_key):
        title = feature_key[key]
        c = plt.scatter(new_data[:,0],new_data[:,1], s=1, c=new_data[:,i+2])
        plt.colorbar(c)
        plt.grid(True)
        plt.title("No Features")
        plt.title("All Architectures, "+ title)
        plt.xlabel("Cost (100 million)")
        plt.ylabel("Reliability (%)")
        #plt.show()
        plt.savefig("metrics_"+title+".png")
        plt.close()
        del c

# Identify a pareto frontier
if 1 == 0:
    fuzz_factor = .05  # Consider less than or equal to the best minus fuzz_factor * best
    pareto_front = np.zeros((sample_size,1), dtype = np.int32)  # 0 for not, 1 for on Pareto Front
    best_cost = 0
    for row in new_data:
        new_cost = row[0]
        new_reliability = row[1]
        if best_cost == 0:
            best_cost = new_cost
            best_reliability = new_reliability
        else:
            # Test to determine if on front
            if new_cost < best_cost*(1 + fuzz_factor) and new_reliability >= best_reliability*(1-fuzz_factor):
                best_cost = new_cost
                best_reliability = new_reliability
    print(best_cost)
    print(best_reliability)
    best_cost = 2 * best_cost  # The best cost fails to capture a fair amount of architectures
    for i,row in enumerate(new_data):
        new_cost = row[0]
        new_reliability = row[1]
        if new_cost <= best_cost*(1+fuzz_factor) and new_reliability >= best_reliability*(1-fuzz_factor):
            pareto_front[i][0] = 1

    if 1 == 1:
        c = plt.scatter(new_data[:,0],new_data[:,1], s=1, c=pareto_front[:,0])
        #plt.colorbar(c)
        plt.grid(True)
        plt.title("No Features")
        plt.title("All Architectures, Fuzzy Pareto Front")
        plt.xlabel("Cost (100 million)")
        plt.ylabel("Reliability (%)")
        #plt.show()
        plt.savefig("metrics_fuzzy_pareto.png")
        plt.close()
        del c

    # Go through and identify any features that occur in the pareto front with a higher probability
    features_in_pareto = np.zeros((10,10),dtype=np.int32)
    features_else_where = np.zeros((10, 10), dtype=np.int32)
    num_of_pareto = 0
    for i in range(new_data.shape[0]):
        if pareto_front[i][0] == 1:
            num_of_pareto += 1
            for j,f in enumerate(new_data[i][3:]):
                features_in_pareto[f][j+2] += 1
        else:
            for j, f in enumerate(new_data[i][3:]):
                features_else_where[f][j+2] += 1

    print(features_else_where)
    print(features_in_pareto)
    features_in_pareto_by_P = np.zeros((10, 10), dtype=np.float)
    features_in_pareto_by_all = np.zeros((10, 10), dtype=np.float)
    for i in range(10):
        for j in range(10):
            features_in_pareto_by_P[i][j] = features_in_pareto[i][j]/num_of_pareto
            if(features_in_pareto[i][j] > 0):
                features_in_pareto_by_all[i][j] = features_in_pareto[i][j] / (features_in_pareto[i][j] + features_else_where[i][j])
    print(features_in_pareto_by_P)
    print(features_in_pareto_by_all)

    #features_in_pareto_by_all.tofile('features in pareto divided by features everywhere.txt',sep=',')
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # turn off summarization, line-wrapping
    with open('features in pareto divided by same features everywhere.txt', 'w') as f:
        f.write(np.array2string(features_in_pareto_by_all, separator=', '))
    with open('features in pareto divided by num in pareto.txt', 'w') as f:
        f.write(np.array2string(features_in_pareto_by_P, separator=', '))
    with open('features in pareto.txt', 'w') as f:
        f.write(np.array2string(features_in_pareto, separator=', '))
    with open('features not in pareto.txt', 'w') as f:
        f.write(np.array2string(features_else_where, separator=', '))