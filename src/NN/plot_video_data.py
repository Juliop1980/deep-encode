import os
import collections
import matplotlib.pyplot as plt


colors_for_resolutions= {234:"#e3d05d",360:"#eb5d80", 432:"#7f86e5",1080:"#7db6e9"}

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

def start_graph(max_bitrate,max_vmaf):
    plt.xlim(0, max_bitrate)
    plt.ylim(0, max_vmaf)
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

prueba = [[72000,1080,33],[722,720,33],[722,540,33]]
prueba2 = [[72000,1080,33],[722,1080,33],[722,1080,33]]

#start_graph(7000,100).show()
#dict = data_dictionary_by_resolution(prueba)
#ord_dict = order_dict_by_key(dict)
#print(ord_dict)
#print(get_list_from_values(ord_dict))
#print(data_dictionary_by_resolution(prueba))
#create_directory("prueba")
#print(order_by_resolution(prueba))
#start_graph_with_max_bitrate_for_video(prueba).show()
print(get_resolution_height(prueba2))
