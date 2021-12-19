import os
import pandas as pd
import pprint

def make_dir(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, name)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory

def get_all_data_prediction(file_path):
    df = pd.read_csv(file_path,delimiter=";")
    df = df.iloc[: , :-1]
    return df

def dict_by_video_id(data):
    data_dict = {}
    for row in data:
        data_dict[row[3]] =[]

    for row in data:
        data_dict[row[3]].append(row[1:])

    return data_dict





#print(make_dir("encodding_ladders"))

#print(get_all_data_prediction('../../data/data_with_predictions_neural_network.csv'))
df = get_all_data_prediction('../../data/data_with_predictions_neural_network.csv')
list = df.values.tolist()
dict_by_video_id = dict_by_video_id(list)
#print(dict_by_video_id)
pprint.pprint(dict_by_video_id)