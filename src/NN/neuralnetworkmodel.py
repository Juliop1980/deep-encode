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
import statistics
from numpy import sqrt 
from scipy.stats import sem

#For jupyter notebook uncomment next line
#%matplotlib inline

# read csv input data
df = pd.read_csv('../../data/pse_data.csv')



#Drop last 3 columns of dataframe, in this case the psnr, vmaf for 4k and vmaf for mobile since these columns are all empty
N = 3
for i in range(N):
        del df[df.columns.values[-1]]

# Here we define the columns that are not numbers as category to calculate a better correlation

df["e_codec_profile"]=df["e_codec_profile"].astype('category').cat.codes
df["c_content_category"]=df["c_content_category"].astype('category').cat.codes
df["s_scan_type"]=df["s_scan_type"].astype('category').cat.codes
df["e_scan_type"]=df["e_scan_type"].astype('category').cat.codes
df["e_pixel_fmt"]=df["e_pixel_fmt"].astype('category').cat.codes

# Calculate the correlation
correlations = df.corr()


# Since we only need to know how the values correlate with the VMAF, we drop all other correlations of the matrix
correlations_with_vmaf = correlations.iloc[: , -1]

# We get the absolute value of the correlations to then order them easily
correlations_with_vmaf = correlations_with_vmaf.abs()

# Order variables with highest correlations with the highest on top
correlations_with_vmaf = correlations_with_vmaf.sort_values(ascending=False)

# We get rid of all the variables that have a correlation of less than 0.04
correlations_with_vmaf = correlations_with_vmaf.iloc[1:9]

# According to the correlations calculated above we extract only these columns from the data plus the VMAF
df1 = df[['e_crf','t_average_bitrate','e_height','e_width','e_scan_type','e_codec_level','e_codec_profile','c_si','t_average_vmaf']]

# Split the data randomly with the train data corresponding to 80% of the data and the test data the remaining 20%
train, test = train_test_split(df1, test_size=0.2)

# Get rid of the vmaf for the train and test data because it is the value we are trying to predict
train_data = train.iloc[: , :-1]
test_data= test.iloc[: , :-1]

# Standardize the data
mean = train_data.mean(axis =0)
std = train_data.std(axis=0)
train_data = (train_data - mean) / std
test_data = (test_data - mean) /std

# Get the correct results for the train and the test data, the value we are trying to predict
train_labels =  train.iloc[: , -1]
test_labels = test.iloc[: , -1]

# Convert the datatype to numpy to reshape the data

train_data_numpy = train_data.to_numpy()
test_data_numpy = test_data.to_numpy()
train_labels_numpy = train_labels.to_numpy()
test_labels_numpy = test_labels.to_numpy()

sample_size = train_data_numpy.shape[0]
time_steps = train_data_numpy.shape[1]
input_dimension =1

# reshape the training data
train_data_reshaped = train_data_numpy.reshape(sample_size,time_steps,input_dimension)

# Function to build the convolutional neural network model

def build_conv1D_model():

  n_timesteps = train_data_reshaped.shape[1] #8

  n_features  = train_data_reshaped.shape[2] #1

  model = keras.Sequential(name="model_conv1D")

  model.add(keras.layers.Input(shape=(n_timesteps,n_features)))

  # Has three convolutional layers (Conv1D_1, Conv1D_2 and Conv1D_3)
  model.add(keras.layers.Conv1D(filters=64, kernel_size=4, activation='relu', name="Conv1D_1"))

  # Add a dropout layer to prevent overfitting
  model.add(keras.layers.Dropout(0.5))

  model.add(keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu', name="Conv1D_2"))

  
  model.add(keras.layers.Conv1D(filters=16, kernel_size=2, activation='relu', name="Conv1D_3"))
  
  # pooling layer
  model.add(keras.layers.MaxPooling1D(pool_size=2, name="MaxPooling1D"))

  # flatten layer
  model.add(keras.layers.Flatten())

  # 2 Hidden layers
  model.add(keras.layers.Dense(32, activation='relu', name="Dense_1"))
  model.add(keras.layers.Dense(n_features, name="Dense_2"))


  optimizer = tf.keras.optimizers.RMSprop(0.001)

  # we use the mse (Mean Square error function) as the loss function and as the metric we use the mean absolute error
  model.compile(loss='mse',optimizer=optimizer,metrics=['mae'])
  return model

# build the model
model_conv1D = build_conv1D_model()

# Prints the details of the model
model_conv1D.summary()

# Uncomment these two lines to train the model and validate with test data
EPOCHS = 500
history = model_conv1D.fit(train_data_reshaped, train_labels_numpy, epochs=EPOCHS, validation_split=0.2, verbose=1)

# Uncomment this line to show the result of the training
#show_history(history)


# Uncomment to get the whole dataset as new data to predict the vmaf
new_data = df1.iloc[: , :-1]
#print(new_data)

#Standardize the data
mean = new_data.mean(axis =0)
std = new_data.std(axis=0)
new_data = (new_data - mean) / std
new_data_labels =  df1.iloc[: , -1]

new_data_numpy = new_data.to_numpy()
new_data_labels_numpy =  new_data_labels.to_numpy()


new_data_reshaped = new_data_numpy.reshape(new_data_numpy.shape[0],new_data_numpy.shape[1],1)

# Uncomment to evaluate the model
[loss, mae] = model_conv1D.evaluate(new_data_reshaped, new_data_labels_numpy, verbose=0)
print("Testing set Mean Abs Error:" + str (mae))

# Uncomment to get predicted vmaf for the whole dataset
test_predictions = model_conv1D.predict(new_data_reshaped).flatten()
#print(test_predictions)
test_predictions = [100 if i >100 else i for i in test_predictions]


df = df[['t_average_bitrate','e_height','s_video_id']]
df["t_average_vmaf_predicted"] = test_predictions
column_names = ['t_average_bitrate', 'e_height', "t_average_vmaf_predicted",'s_video_id']
df = df.reindex(columns=column_names)

df.to_csv('data_with_predictions.csv', index=False, sep = ';')

# Uncomment to get the MAE and a standard error, you can set the repeats but be aware that it takes longer with more repeats

#repeats = 200
#scores = list()
#for i in range(repeats):
#	#train, test = train_test_split(df1, test_size=0.2)
#	train, test = train_test_split(df1, test_size=0.2)
#	train_data = train.iloc[: , :-1]
#	test_data= test.iloc[: , :-1]
#	mean = train_data.mean(axis =0)
#	std = train_data.std(axis=0)
#	train_data = (train_data - mean) / std
#	test_data = (test_data - mean) /std
#	train_labels =  train.iloc[: , -1]
#	test_labels = test.iloc[: , -1]
#	train_data_numpy = train_data.to_numpy()
#	test_data_numpy = test_data.to_numpy()
#	train_labels_numpy = train_labels.to_numpy()
#	test_labels_numpy = test_labels.to_numpy()
#	sample_size = train_data_numpy.shape[0]
#	time_steps = train_data_numpy.shape[1]
#	input_dimension =1
#	train_data_reshaped = train_data_numpy.reshape(sample_size,time_steps,input_dimension)
#	#model = fit(train.X, train.y)
#	EPOCHS = 500
#	history = model_conv1D.fit(train_data_reshaped, train_labels_numpy, epochs=EPOCHS, validation_split=0.2, verbose=1)
#	test_data_reshaped = test_data_numpy.reshape(test_data_numpy.shape[0],test_data_numpy.shape[1],1)

#	[loss, mae] = model_conv1D.evaluate(test_data_reshaped, test_labels_numpy, verbose=0)
#	skill = mae
#	scores.append(skill)

#mean_skill = statistics.mean(scores)
#print("number of tests =  200")
#print("mean :" + str(mean_skill))

##standard_deviation = sqrt(1/len(scores) * sum( (score - mean_skill)^2 ))
#standard_error = sem(scores)

##interval = standard_error * 1.96
#lower_interval = mean_skill - standard_error
#upper_interval = mean_skill + standard_error


#print("standard_error :" + str(standard_error))
#print("lower_interval :" + str(lower_interval))
#print("upper_interval :" + str(lower_interval))
##print(lower_interval)
##print(upper_interval)


