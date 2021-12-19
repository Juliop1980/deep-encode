import os
import pandas as pd
import pprint

list_of_bitrate = [235,375,560,750,1050,1750,2350,3000,4300,5800]

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
        data_dict[row[3]].append(row)

    #print(data_dict)
    return data_dict

def create_dict_by_range():
    data_dict = {}
    for row in list_of_bitrate:
        data_dict[row] =[]

    return data_dict

def get_range_bitrate(bitrate):
    if bitrate <375:
        return 235
    elif bitrate <560:
        return 375
    elif bitrate < 750:
        return 560
    elif bitrate < 1050:
        return 750
    elif bitrate < 1750:
        return 1050
    elif bitrate < 2350:
        return 1750
    elif bitrate < 3000:
        return 2350
    elif bitrate < 4300:
        return 3000
    elif bitrate < 5800:
        return 4300
    else:
        return 5800




def separate_by_range(lists_of_rows):
    dict_by_bitrate = create_dict_by_range()
    for row in lists_of_rows:
        bitrate = row[0]
        #print(bitrate)
        range= get_range_bitrate(bitrate)
        #print(range)
        dict_by_bitrate[range].append(row[1:])

    return dict_by_bitrate

def get_list_with_certain_vmaf(lists,vmaf):
    for list in lists:
        if list[1] == vmaf:
            return list
        
def get_data_with_most_vmaf(lists):
    vmaf = 0
    for row in lists:
        vmaf = max(vmaf,row[1])
    #print(vmaf)
    list =get_list_with_certain_vmaf(lists,vmaf)
    return list

    
    #print(dict_by_bitrate)

def get_resolution(list):
    resolution_width = list[0]
    resolution_heigth = dict_resolution[resolution_width]


#print(make_dir("encodding_ladders"))

#print(get_all_data_prediction('../../data/data_with_predictions_neural_network.csv'))
df = get_all_data_prediction('../../data/data_with_predictions_neural_network.csv')
list = df.values.tolist()
dict_by_video_id = dict_by_video_id(list)
list_video = dict_by_video_id[418]
#print(dict_by_video_id)
#pprint.pprint(dict_by_video_id)
#pprint.pprint(separate_by_range(list))

list_by_range=separate_by_range(dict_by_video_id[418])[235]
print(get_data_with_most_vmaf(list_by_range))
