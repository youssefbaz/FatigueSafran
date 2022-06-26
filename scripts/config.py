import os
import streamlit as st
from datetime import date, datetime
# define the base path to the input data
import statistics




def init_session(demoMode=False):
    from streamlit.scriptrunner import add_script_run_ctx
    session_id=add_script_run_ctx().streamlit_script_run_ctx.session_id
    print("session id "+str(session_id))
    session_path = os.path.join(os.path.dirname(__file__), "../data/sessions/")
    if not os.path.exists(session_path):
        os.mkdir(session_path)
    path=os.path.join(session_path,str(date.today())+"_"+session_id)
    if demoMode:
        path=os.path.join(os.path.dirname(__file__), "../data/demo")
    if not os.path.exists(path):
        print("init session on "+path)
        os.mkdir(path)
        os.sync()
        print("Directory '%s' created successfully" %path)
        os.mkdir(os.path.join(path,"processed"))
        os.mkdir(os.path.join(path,"raw"))
        os.sync()
        os.mkdir(os.path.join(path,"raw","finite_elements"))
        os.mkdir(os.path.join(path,"raw","experimental"))
        os.sync()
        for section in ["finite_elements","experimental","parameters", "images"]:
            os.mkdir(os.path.join(path,"processed", section))
        with open(os.path.join(path,"_session_config.py"),"w") as session_config:
            session_config.write("creation_date="+str(datetime.now()))
    else:
        print("config already exist in "+ path)
    return path

path= init_session()

BASE_PATH=os.path.abspath(path)

# input 
RAW_DATA_PATH = os.path.sep.join([BASE_PATH, "raw", "finite_elements" ])
# Test_results_different_scales_CHP.txt
EXPERIMENTAL_PATH = os.path.sep.join([BASE_PATH, "raw", "experimental" ])
#DEMO_EXPERIMENTAL_PATH = os.path.join([os.path.dirname(__file__), "../data/experimental"])

# output
PROCESSED_DATA_PATH = os.path.sep.join([BASE_PATH, "processed", "finite_elements"])

#read data from experimental file
PROCESSED_DATA_EXP = os.path.sep.join([BASE_PATH, "processed", "experimental"])
DEMO_PROCESSED_DATA_EXP = os.path.join(os.path.dirname(__file__), "../data/demo/processed/experimental")
#get the Observed_Nf and Nf_list data from experimental data
DEST_N0 =os.path.sep.join([BASE_PATH, "processed", "parameters",'met_5.csv'])
# images path fo bayesian (no more needed ?)
IMAGES_PATH = os.path.sep.join([BASE_PATH, "processed", "images" ])

import csv


met={}
def get_met():
    global met, DEST_N0
    if os.path.exists(DEST_N0):
        print("met present")
        with open(DEST_N0, mode='r') as inp:
            reader_met = csv.reader(inp, delimiter=",")
            next(reader_met)
            met = {row[0]:float(row[6]) for row in reader_met}
            print("readed met ", met)
    else:
        print("no met in "+DEST_N0)
    return met
print("** import")
get_met()
print("** done import")

def get_nf():
    global Nf_list, observed_Nf,DEST_N0
    Nf_list=[]
    observed_Nf = []
    if os.path.exists(DEST_N0):
        #with open(DEMO_PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv") as f:
        with open(PROCESSED_DATA_EXP+"/Test_results_different_scales_CHP.csv") as f:
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
    else:
        print(" no scales in "+DEST_N0)
    return Nf_list, observed_Nf

Nf_list, observed_Nf = get_nf()

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

