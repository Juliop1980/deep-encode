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

N = 3
#Drop last N columns of dataframe
for i in range(N):
        del df[df.columns.values[-1]]

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

#df.drop(df.tail(4).index,inplace=True) # drop last 3 rows

correlations = df.corr()
#print(correlations)

#correlations_with_target_resolution = correlations.iloc[: , -4]
##print(correlations_with_vmaf)
#correlations_with_vmaf = correlations_with_vmaf.abs()
#correlations_with_vmaf = correlations_with_vmaf.sort_values(ascending=False)
##print(correlations_with_vmaf)
#correlations_with_vmaf.drop(correlations_with_vmaf.tail(9).index,inplace=True)
#print(correlations_with_vmaf)


correlations_with_vmaf = correlations.iloc[: , -1]
#print(correlations_with_vmaf)
correlations_with_vmaf = correlations_with_vmaf.abs()
correlations_with_vmaf = correlations_with_vmaf.sort_values(ascending=False)
#print(correlations_with_vmaf)
correlations_with_vmaf = correlations_with_vmaf.iloc[1:9]
#print(correlations_with_vmaf)

df1 = df[['e_crf','t_average_bitrate','e_height','e_width','e_scan_type','e_codec_level','e_codec_profile','c_si','t_average_vmaf']]
#print(df1)
#train, test = train_test_split(df, test_size=0.2)
#train.to_csv('train_data.csv')
#test.to_csv('test_data.csv')