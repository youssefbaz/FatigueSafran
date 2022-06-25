import os
import streamlit as st

# define the base path to the input data
import statistics

BASE_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../data"))

RAW_DATA_PATH = os.path.sep.join([BASE_PATH, "raw", ])
PROCESSED_DATA_PATH = os.path.sep.join([BASE_PATH, "processed", "finite_elements"])

#read data from experimental file
PROCESSED_DATA_EXP = os.path.sep.join([BASE_PATH, "processed", "experimental"])
#get the Observed_Nf and Nf_list data from experimental data
DEST_N0 =os.path.sep.join([BASE_PATH, "processed", "parameters","damage_parameter",'met_5.csv'])

import csv

Nf_list=[]
observed_Nf = []

met={}
if os.path.exists(DEST_N0):
    with open(DEST_N0, mode='r') as inp:
        reader_met = csv.reader(inp, delimiter=",")
        next(reader_met)
        met = {row[0]:float(row[6]) for row in reader_met}

Nf_list=[]
if os.path.exists(DEST_N0):
    with open(PROCESSED_DATA_EXP+"\\Test_results_different_scales_CHP.csv") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        d={}
        for row in reader:
            value = int(float(row[0]))
            observed_Nf.append(value)
            if not row[1] in d:
                d[row[1]]=[]
            d[row[1]].append(value)
        dict_means={}
        for k in d.keys():
            dict_means[k]=statistics.mean(d[k])
        Nf_list=list(dict_means.values())
        print(observed_Nf)
        print(Nf_list)

# DIFFERENTIATE INITIAL BN FROM EXP DATA IN THE LIKELIHOOD AND THE BN IN THE PRIOR WHICH AR HE BELIEFS
bn_init_values = (1.149, 0.7)
bn_priors = (1.45, 0.32)

# Constants (to put as parameters later on)
#bserved_Nf = [10275, 19773, 50119, 171907, 5196, 25347, 50573, 100453, 11348, 12533, 15287, 135323, 17504, 19773,
              # 35562, 38922, 42793, 50119, 55855, 69058, 78364, 101364]
# fix one random state :
RANDOM_SEED = 5690

# Dict of parameters used for likelihood function
#NO_w Coming from the damage parameter calculation: taken as constant for now

SKIPROWS = 19
SKIPFOOTER = 9

# damage parameters
scale_sizes = ["100", "80", "60", "40"]
# Taken from the main papper:
material_param_delta0 = -1.97
##
#C = 3.45e3
##bn =bn_init_values[0]
# this value is taken from this paper:
# https://www.sciencedirect.com/science/article/abs/pii/S0013794418302169
m = 9.10

gamma_dict = {1.74: 948.9222196304526,
              2.78: 1225.1311269056903,
              3.86: 1076.7142360993241,
              6.63: 1106.2997786001345}

# take Nf_list for te likelihood formula as mean of each subclass of experimental data
#Nf_list = [50931, 43623, 45392, 63018]

# Coming from the damage parameter calculation: taken as constant for now
#N0_w = 948.922
sigma_eps = 0.01

default_params = {
    'gamma':1.74,
    'sigma_eps': sigma_eps,
    'Nf_list': Nf_list,
    'observed_Nf': observed_Nf,
    'c':3.45e3,
    'k': 1.75,
    'bn_mean':1.149,
    'bn_std':0.7
}

