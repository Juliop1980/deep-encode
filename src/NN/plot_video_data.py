import os
import collections
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
import pandas as pd


colors_for_resolutions= {234:"#e3d05d",360:"#eb5d80", 432:"#7f86e5",540:"#f1a062",720:"#424346",1080:"#7db6e9"}
resolution_height_width_dict = {234:416,360:640, 432:768,540:960,720:1280,1080:1920}

def create_directory(directory_name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, directory_name)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory

def data_dictionary_by_resolution(list_of_data_by_resolution):
    dictionary = {}
    for i in list_of_data_by_resolution:
        resolution = i[1]
        dictionary[resolution] = i
    return dictionary

def order_dict_by_key(dict):
     return collections.OrderedDict(sorted(dict.items()))

def get_list_from_values(dict):
    values = dict.values()
    values_list = list(values)
    return values_list

def order_by_resolution(list_of_data_by_resolution):
    dict = data_dictionary_by_resolution(list_of_data_by_resolution)
    dictionary_by_resolution = order_dict_by_key(dict)
    final_ordered_list = get_list_from_values(dictionary_by_resolution)
    return final_ordered_list

def get_max_bitrate(data_list_video):
    max_bitrate = 0
    for i in data_list_video:
        if max_bitrate<i[0]:
            max_bitrate = i[0]
    return max_bitrate

def start_graph(max_bitrate,max_vmaf,title):
    plt.xlim(0, max_bitrate)
    plt.ylim(0, max_vmaf)
    plt.title(title)
    return plt

def start_graph_with_max_bitrate_for_video(data_for_video_in_lists):
    max_bitrate = get_max_bitrate(data_for_video_in_lists)
    graph = start_graph(max_bitrate, 100)
    return graph

def get_resolution_height(lists_with_resolution):
    first_list_with_resolution = lists_with_resolution[0]
    resolution_height = first_list_with_resolution[1]
    return resolution_height

def get_color_for_resolution(resolution_height):
    color_hexadecimal = colors_for_resolutions[resolution_height]
    return color_hexadecimal

def get_bitrate(datos):
    bitrate = datos[0]
    return bitrate

def get_vmaf(datos):
    vmaf = datos[2]
    return vmaf

#def get_all_points_with_label(resolution_height,graph):


def plot_smooth_resolution_graph(x_points_list,y_points_list,resolution_height,graph):
    xnew = np.linspace(min(x_points_list), max(x_points_list), 300) 
    spl = make_interp_spline(x_points_list, y_points_list, k=3)  # type: BSpline
    power_smooth = spl(xnew)
    label_graph = str(resolution_height_width_dict[resolution_height]) + "x" + str(resolution_height)
    graph.plot(xnew,power_smooth,label = label_graph,color=get_color_for_resolution(resolution_height))
    graph.legend()
    return graph


def store_graph_directory(graph, video_id):
    path = str(video_id) + "/graph.png"
    graph.savefig(path)
    return (str(video_id) + "/graph.png")



#prueba = [[72000,1080,33],[722,720,33],[722,540,33]]
#prueba2 = [[72000,1080,33],[722,1080,33],[722,1080,33]]

# line 1 points
#x1 = [1,2,3]
#y1 = [2,4,1]
## plotting the line 1 points
##plt.plot(x1, y1, label = "line 1")
 
## line 2 points
#x2 = [1,2,3]
#y2 = [4,1,3]
## plotting the line 2 points
##plt.plot(x2, y2, label = "line 2")
 
## naming the x axis
##plt.xlabel('x - axis')
## naming the y axis
##plt.ylabel('y - axis')
## giving a title to my graph
##plt.title('Two lines on same graph!')
 
## show a legend on the plot
##plt.legend()
 
##start_graph(7000,100).show()
##dict = data_dictionary_by_resolution(prueba)
##ord_dict = order_dict_by_key(dict)
##print(ord_dict)
##print(get_list_from_values(ord_dict))
##print(data_dictionary_by_resolution(prueba))
##create_directory("prueba")
##print(order_by_resolution(prueba))
##start_graph_with_max_bitrate_for_video(prueba).show()
##print(get_resolution_height(prueba2))
##print(get_color_for_resolution(432))
##datos = [72000,1080,33]
##print(get_vmaf(datos))
##smooth_resolution_graph(100,plt).show()

#x1 = [1,2,3,4,5]
#y1 = [3,5,7,12,20]
## plotting the line 1 points
##plt.plot(x1, y1, label = "line 1")

##xnew = np.linspace(min(x1), max(x1), 300) 
##spl = make_interp_spline(x1, y1, k=3)  # type: BSpline
##power_smooth = spl(xnew)
##plt.plot(xnew, power_smooth)
##plt.show()
##plot_smooth_resolution_graph(x1,y1,1080,plt).show()
##graph =start_graph(7000,100,"encodding_ladder")

#graph  = plot_smooth_resolution_graph(x1,y1,1080,plt)
#store_graph_directory(graph, 123)

df = pd.read_csv('../../data/pse_data.csv')

s_video_ids = df["s_video_id"].tolist()
s_video_ids = list(set(s_video_ids))
s_video_ids.sort()

for i in s_video_ids:
    print(i)








