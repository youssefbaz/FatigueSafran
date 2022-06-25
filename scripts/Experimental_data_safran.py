import os
import re
import glob
import pandas as pd
import numpy as np
import plotly.express as px
import math
from itertools import combinations
import data_utils


# Get data from txt and rpt folder:
# make sure the "Data" folder is in the same directory as the py code

txt_files = glob.glob(os.path.join(os.getcwd(),"**\\*.txt"),recursive=True)
rpt_files = glob.glob(os.path.join(os.getcwd(),"**\\*.rpt"),recursive=True)

# Get experimental data and make experimental dataframe: not in module cause data source may change
'''experimental_txt = []

with open(txt_files[2], "r") as f:
  experimental_txt = f.readlines()

experimental_txt = [i.replace("\t","$").replace("\n","") for i in experimental_txt]
reg = r'\d+\$\d+'
experimental_txt = [re.findall(reg,i)[0].split('$') for i in experimental_txt if len(re.findall(reg,i))>0]
experimental_df = pd.DataFrame(experimental_txt,columns=['LCF','Specimen']).astype(float)
experimental_df['Specimen'] = experimental_df['Specimen'].apply(lambda x:int(x))
'''

def make_VN_vector(df,col_V,col_N):
    tuples_list = list(zip(df[col_V], round(df[col_N],2)))
    #tuples_list = tuples_list[::-1]
    print("tuple_list")
    print(tuples_list)
    print("combi tuple")

    V_N_vector = []
    for i in combinations(tuples_list,2):
        # if i[0][0]!=i[1][0] and i[0][1]!=i[1][1]
        # to avoid "extreme values" we must make sure N1 is different ENOUGH from N2 : ie N1 and N2 are more than 1% different
        # but not more than 20 times more than N2
        if i[0][0]!=i[1][0] and i[0][1] > 1.2*i[1][1] and i[0][1] < 3*i[1][1] :
            V_N_vector.append((i[0][0],i[0][1],i[1][0],i[1][1])) # tuple (V1,N1,V2,N2)
    return V_N_vector




def set_small_to_zero(a,eps):
  a[np.abs(a) < eps] = 0
  return a


def calculate_Bn(v):
    V1,N1,V2,N2 = v
    print("V1 is {}, v2 is {}, N1 is {} and N2 is {}".format(V1,V2,N1,N2))
    bn = round((math.log(V2)-math.log(V1))/(math.log(N1)-math.log(N2)),4)
    print(bn)
    return bn

def Bn_data(tuple_list):
    Bn_data = []
    for i in tuple_list:
        Bn_data.append(calculate_Bn(i))
    print(Bn_data)
    print("Bn mean is : " + str(round(np.mean(Bn_data),3)))
    print("Bn std is : " + str(round(np.std(Bn_data),3)))
    return Bn_data,np.mean(Bn_data),np.std(Bn_data)


def show_histogram(values_list):
  histo_bn = px.histogram(x=values_list,nbins=20,template='simple_white')
  histo_bn.show()


#print('Bn only positive ---------------------------------')
#positive_V_N = make_VN_vector(df=experimental_df, col_V='Specimen', col_N='LCF')
#Bn_positive, Bn_positive_mean, Bn_positive_std = Bn_data(positive_V_N)
#show_histogram(Bn_positive)


if __name__=='__main__':
    # Reading the processed file
    _, EXP_paths = data_utils.get_paths()
    _, expmtl_processed_paths = EXP_paths
    print(expmtl_processed_paths[0])
    experimental_df = data_utils.read_processed_data(expmtl_processed_paths[0])

    print(experimental_df)

    # show scatter plot for experimental data

    #graph = px.scatter(experimental_df, x=experimental_df['LCF'],
    #                   y=experimental_df['Specimen'],
    #                   template='simple_white',
    #                   symbol='Specimen')
    #graph.update_yaxes(type='category')
    #graph.update_traces(marker_size=10)
    #graph.show()


    # 5. as V2/V1 > 1, and bn must be > 0 remove combi that does not give N1>N2
    print('Bn only positive ---------------------------------')
    positive_V_N = make_VN_vector(df=experimental_df, col_V='Specimen', col_N='LCF')
    Bn_positive, Bn_positive_mean, Bn_positive_std = Bn_data(positive_V_N)
    show_histogram(Bn_positive)
#bn initializartion script (minor change about the path )

