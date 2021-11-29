import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
#For jupyter notebook uncomment next line
#%matplotlib inline

df = pd.read_csv('../../data/pse_data.csv')
#print(df.head())
#df.head()

#df.drop(df.tail(3).index,inplace=True) # drop last 3 rows

#N = 3
## Drop last N columns of dataframe
#for i in range(N):
#        del df[df.columns.values[-1]]

#print(df.isnull().sum())
#index = df.index
#number_of_rows = len(index)
#print(number_of_rows)

#print(df.info())
#print(df["e_codec_profile"])
df["e_codec_profile"]=df["e_codec_profile"].astype('category').cat.codes
df["c_content_category"]=df["c_content_category"].astype('category').cat.codes
df["s_scan_type"]=df["s_scan_type"].astype('category').cat.codes
df["e_scan_type"]=df["e_scan_type"].astype('category').cat.codes
df["e_pixel_fmt"]=df["e_pixel_fmt"].astype('category').cat.codes


correlations = df.corr()
#print(correlations)
correlations_with_vmaf = correlations.iloc[: , -4]
#print(correlations_with_vmaf)
correlations_with_vmaf = correlations_with_vmaf.abs()
correlations_with_vmaf = correlations_with_vmaf.sort_values(ascending=False)
#print(correlations_with_vmaf)
correlations_with_vmaf.drop(correlations_with_vmaf.tail(9).index,inplace=True)
print(correlations_with_vmaf)
