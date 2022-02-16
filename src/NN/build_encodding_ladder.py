# Script to build the encodding ladder for every video with the predicted data calculated in previous steps
import os
import pandas as pd
import pprint
from matplotlib import pyplot as plt
import numpy as np

list_of_bitrate = [235,375,560,750,1050,1750,2350,3000,4300,5800]
dict_resolution = {234:416,360:640, 432:768,540:960,720:1280,1080:1920}

# make directory in current path with given name
def make_dir(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, name)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory

# get the data with the predicted vmaf looking in the path given
def get_all_data_prediction(file_path):
    df = pd.read_csv(file_path,delimiter=";")
    df = df.iloc[: , :-1]
    return df

# get dictionary with the key being the video id and the value a list of lists of all the data for that particular video
def dict_by_video_id(data):
    data_dict = {}
    for row in data:
        data_dict[row[3]] =[]

    for row in data:
        data_dict[row[3]].append(row)

    #print(data_dict)
    return data_dict

# creates an empty dictionary with the keys being the bitrate values in which netflix splits their encodding ladder
def create_dict_by_range():
    data_dict = {}
    for row in list_of_bitrate:
        data_dict[row] =[]

    return data_dict

# get the bitrate range in which a certain bitrate is categorized in the encodding ladder
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
     
        range= get_range_bitrate(bitrate)
    
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

def get_resolution(list):
    resolution_width = list[0]
    resolution_height = dict_resolution[resolution_width]
  
    resolution =str(resolution_height) + "x"+ str(int(resolution_width))
    return resolution

def get_video_id(list):
    return int(list[2])

def get_vmaf(list):
    return list[1]

def make_results_in_lists(x,y,z):
    return [x,y,z]

def get_path(video_id):
    path =os.path.join("encodding_ladders",str(video_id),"encodding_ladder.pdf")
    return path

def store_in_pdf(ladder,path,video_id):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    y=np.array([np.array(xi) for xi in ladder])
    df = pd.DataFrame(y, columns=["Bitrate (kbps)", "Resolution", "VMAF (Predicted)"])
    ax.table(cellText=df.values, colLabels=df.columns, loc='center',cellLoc='center')
    fig.tight_layout()
 
    plt.title('Video ' + str(video_id) )
    plt.savefig(path, bbox_inches='tight')
    plt.clf()
    return plt

def store_encodding_ladder(video_id,ladder):
    dir_path = get_path(video_id)
    make_dir("encodding_ladders\\" + str(video_id))

    graph = store_in_pdf(ladder,dir_path,video_id)

    return graph

def write_to_csv(dataframe,path):
    dataframe.to_csv(path + '/results.csv', mode='a', header =False,index=False)
    return(path + '/results.csv')

def store_in_excel_encodding_ladder(video_id,encodding_ladder):
    current_path = os.getcwd()
    for i in encodding_ladder:
        i.insert(0,str(video_id))
    y=np.array([np.array(xi) for xi in encodding_ladder])
    df = pd.DataFrame(y, columns=["Video ID", "Bitrate (kbps)", "Resolution", "VMAF (Predicted)"])
    path = write_to_csv(df,current_path)
    return path


file_path='data_with_predictions.csv'
make_dir("encodding_ladders")
final_result = []
data = get_all_data_prediction(file_path)

list_value = data.values.tolist()

separated_data =dict_by_video_id(list_value)
for key in separated_data:
    ladder_result=[]
    make_dir("encodding_ladders\\"+ str(int(key)))
    lists_of_data =separated_data[key]
 
    dict_by_bitrate_range = separate_by_range(lists_of_data)
  
    for key in dict_by_bitrate_range:
        best_vmaf= get_data_with_most_vmaf(dict_by_bitrate_range[key])
        if best_vmaf == None:
            temp = list(dict_by_bitrate_range)
            if key != 5800:
                res = temp[temp.index(key) + 1]
                best_vmaf= get_data_with_most_vmaf(dict_by_bitrate_range[res])

            if key==5800:
                res = temp[temp.index(key) - 1]
                best_vmaf= get_data_with_most_vmaf(dict_by_bitrate_range[res])

        bitrate=key
        resolution = get_resolution(best_vmaf)
        video_id=get_video_id(best_vmaf)
        vmaf=get_vmaf(best_vmaf)
        list_result = make_results_in_lists(bitrate,resolution,vmaf)
        ladder_result.append(list_result)


            #final_result.append(list_result)

    #print(video_id)
    #graph= store_encodding_ladder(video_id, ladder_result)
    #graph.clf()

    store_in_excel_encodding_ladder(video_id,ladder_result)
    columns=["Video ID", "Bitrate (kbps)", "Resolution", "VMAF (Predicted)"]
    #file = pd.read_csv("results.csv")
    #file.to_csv("results.csv", header=columns, index=False)
        

    
    #print(final_result)
