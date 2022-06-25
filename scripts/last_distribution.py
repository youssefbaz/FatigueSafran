

#import librairies 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from fitter import Fitter, get_common_distributions, get_distributions


# In[6]:

def compute_distribution():

#read the data file 
    data= pd.read_csv("../data/raw/experimental/Test_results_different_scales_CHP.txt",skiprows = 1, sep = '\t'
                   , names = ['LCF', 'Specimen'], header = 0
                   , dtype = {'LCF': np.int64, 'Specimen': np.int64})

    #retrieve the data for every scale respectively 40,60,80,100
    df_scale_40 = data.loc[data['Specimen'] == 40]
    df_scale_60 = data.loc[data['Specimen'] == 60]
    df_scale_80 = data.loc[data['Specimen'] == 80]
    df_scale_100 = data.loc[data['Specimen'] == 100]

    scale_size=[df_scale_40,df_scale_60,df_scale_80,df_scale_100]
    print(df_scale_40)
compute_distribution()
  ###  for scale in range(len(scale_size)):
     #   f = Fitter(df_scale_40['LCF'], distributions=['gamma','lognorm',"beta","burr","norm",'exponnorm', 'exponpow', 'exponweib'])
     #   f.fit()
      #  print(f.summary())
       # print(f.get_best(method = 'sumsquare_error'))
#The Fitter class uses the Scipy library which supports 80 distributions and the Fitter class will scan all of them,
#call the fit function for you, give you a summary of the best distributions in the sense of sum of the square errors.
#get the best distribution for the scale 40 
#f = Fitter(df_scale_40['LCF'], distributions=['gamma','lognorm',"beta","burr","norm",'exponnorm', 'exponpow', 'exponweib'])
#f.fit()
#print(f.summary())
#print(f.get_best(method = 'sumsquare_error'))


# In[33]:


#get the best distribution for the scale 60 
#f = Fitter(df_scale_60['LCF'], distributions=['gamma','lognorm',"beta","burr","norm",'exponnorm', 'exponpow', 'exponweib'])
#f.fit()
#print(f.summary())
#print(f.get_best(method = 'sumsquare_error'))


# In[30]:


#get the best distribution for the scale 80
#f = Fitter(df_scale_80['LCF'], distributions=['gamma','lognorm',"beta","burr","norm",'exponnorm', 'exponpow', 'exponweib'])
#f.fit()
#print(f.summary())
#print(f.get_best(method = 'sumsquare_error'))


# In[34]:


#get the best distribution for the scale 100
#f = Fitter(df_scale_100['LCF'], distributions=['gamma','lognorm',"beta","burr","norm",'exponnorm', 'exponpow', 'exponweib'])
#f.fit()
#print(f.summary())
#print(f.get_best(method = 'sumsquare_error'))


# In[35]:


#get the best distributions without taking into account the scale
#f = Fitter(data['LCF'], distributions=['gamma','lognorm',"beta","burr","norm",'exponnorm', 'exponpow', 'exponweib'])
#f.fit()
#print(f.summary())
#print(f.get_best(method = 'sumsquare_error'))





