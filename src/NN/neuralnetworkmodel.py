import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import Model
from plot_keras_history import show_history, plot_history
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
#train = train.iloc[: , 0:]
train, test = train_test_split(df1, test_size=0.2)
train_data = train.iloc[: , :-1]
test_data= test.iloc[: , :-1]
#train = train.iloc[: , 0:]
#print(train)
#test = test.iloc[: , 0:]
#print(test)
#train.to_csv('train_data.csv',index=False)
#test.to_csv('test_data.csv',index=False)
mean = train_data.mean(axis =0)
std = train_data.std(axis=0)
train_data = (train_data - mean) / std
test_data = (test_data - mean) /std
train_labels =  train.iloc[: , -1]
test_labels = test.iloc[: , -1]
train_data_numpy = train_data.to_numpy()
test_data_numpy = test_data.to_numpy()
train_labels_numpy = train_labels.to_numpy()
test_labels_numpy = test_labels.to_numpy()
#print(train_labels_numpy[0:10])
#train_data.to_csv('train_data.csv',index=False)
#test_data.to_csv('test_data.csv',index=False)
#train_labels.to_csv('train_labels.csv',index=False)
#test_labels.to_csv('test_labels.csv',index=False)
#print(train_data.iloc[0])
#print(test_data.iloc[0])
#print(train_labels.iloc[0:10])
#print(test_labels.iloc[0:10])
#train.to_csv('train_data.csv',index=False)
#print(train_data_numpy.shape)
#print(train_data_numpy[0])
sample_size = train_data_numpy.shape[0]
time_steps = train_data_numpy.shape[1]
input_dimension =1
train_data_reshaped = train_data_numpy.reshape(sample_size,time_steps,input_dimension)
#print(time_steps)

#print("After reshape train data set shape:\n", train_data_reshaped.shape)
#print("1 Sample shape:\n",train_data_reshaped[0].shape)
#print("An example sample:\n", train_data_reshaped[0])

def build_conv1D_model():

  n_timesteps = train_data_reshaped.shape[1] #8
  print(n_timesteps)
  n_features  = train_data_reshaped.shape[2] #1

  model = keras.Sequential(name="model_conv1D")

  model.add(keras.layers.Input(shape=(n_timesteps,n_features)))

  model.add(keras.layers.Conv1D(filters=64, kernel_size=4, activation='relu', name="Conv1D_1"))
  model.add(keras.layers.Dropout(0.5))

  model.add(keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu', name="Conv1D_2"))

  print("-------------------------------------------------------------")
  
  model.add(keras.layers.Conv1D(filters=16, kernel_size=2, activation='relu', name="Conv1D_3"))
  
  model.add(keras.layers.MaxPooling1D(pool_size=2, name="MaxPooling1D"))
  model.add(keras.layers.Flatten())
  model.add(keras.layers.Dense(32, activation='relu', name="Dense_1"))
  model.add(keras.layers.Dense(n_features, name="Dense_2"))


  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',optimizer=optimizer,metrics=['mae'])
  return model

model_conv1D = build_conv1D_model()
model_conv1D.summary()

EPOCHS = 500
history = model_conv1D.fit(train_data_reshaped, train_labels_numpy, epochs=EPOCHS, validation_split=0.2, verbose=1)

#show_history(history)
#plot_history(history, path="standard.png")
#plt.close()
#print(len(test_data_numpy))
test_data_reshaped = test_data_numpy.reshape(test_data_numpy.shape[0],test_data_numpy.shape[1],1)

[loss, mae] = model_conv1D.evaluate(test_data_reshaped, test_labels_numpy, verbose=0)
print("Testing set Mean Abs Error:" + str (mae))



test_predictions = model_conv1D.predict(test_data_reshaped).flatten()


