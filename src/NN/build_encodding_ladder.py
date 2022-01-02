import os
import pandas as pd
import pprint
from matplotlib import pyplot as plt
import numpy as np

list_of_bitrate = [235,375,560,750,1050,1750,2350,3000,4300,5800]
dict_resolution = {234:416,360:640, 432:768,540:960,720:1280,1080:1920}
#print(type(dict_resolution))
#print(dict_resolution[234])

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
    #print(type(dict_resolution))
    #print(resolution_width )
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
    #path = "encodding_ladders" + "\\\\"+ str(video_id) + "\\\\" +"encodding_ladder.pdf"
    path =os.path.join("encodding_ladders",str(video_id),"encodding_ladder.pdf")
    return path

def store_in_pdf(ladder,path,video_id):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    #print(np.random.randn(10, 3))
    y=np.array([np.array(xi) for xi in ladder])
    df = pd.DataFrame(y, columns=["Bitrate (kbps)", "Resolution", "VMAF (Predicted)"])
    ax.table(cellText=df.values, colLabels=df.columns, loc='center',cellLoc='center')
    fig.tight_layout()
    #plt.show()
    plt.title('Video ' + str(video_id) )
    plt.savefig(path, bbox_inches='tight')

def store_encodding_ladder(video_id,ladder):
    dir_path = get_path(video_id)
    make_dir("encodding_ladders\\" + str(video_id))

    store_in_pdf(ladder,dir_path,video_id)
    #ath = "plots\\" + str(video_id) + "\\graph.png"
    #raph.savefig(path)
    return (dir_path)

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



#print(make_dir("encodding_ladders"))

#print(get_all_data_prediction('../../data/data_with_predictions_neural_network.csv'))
#df = get_all_data_prediction('../../data/data_with_predictions_neural_network.csv')
#list_value = df.values.tolist()
#dict_by_video_id = dict_by_video_id(list_value)
#list_video = dict_by_video_id[418]
#print(dict_by_video_id)
#pprint.pprint(dict_by_video_id)
#pprint.pprint(separate_by_range(list))

#list_by_range=separate_by_range(dict_by_video_id[418])[235][0]
#print(get_data_with_most_vmaf(list_by_range))
#print(get_resolution(list_by_range))
#print(get_video_id(list_by_range))

#print(get_vmaf(list_by_range))

#print(make_results_in_lists(get_video_id(list_by_range),get_vmaf(list_by_range),2))
#print(get_path(418))

#ladder = [[235, "320x240",99], [375, "384x288",100],[560,"512x384",100], [750,"512x384",100],[1050,"512x384",100],[1750,"512x384",100],[2350,"512x384",100],[3000,"512x384",100],[4300,"512x384",100],[5800,"512x384",100]]
#store_encodding_ladder(418, ladder)
#store_in_excel_encodding_ladder(418, ladder)

make_dir("encodding_ladders")