import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
#For jupyter notebook uncomment next line
#%matplotlib inline

df = pd.read_csv('../../data/pse_data.csv')
print(df.head())
#df.head()