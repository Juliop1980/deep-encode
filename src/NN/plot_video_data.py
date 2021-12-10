import os

def create_directory(directory_name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, directory_name)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    return final_directory

def order_by_resolution(list_of_data_by_resolution):


#create_directory("prueba")
