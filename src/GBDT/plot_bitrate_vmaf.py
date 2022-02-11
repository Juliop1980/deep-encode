# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.spatial import ConvexHull

df = pd.read_csv('predicted_vmaf.csv')

video_id = pd.unique(df['s_video_id']).astype(int)
e_width_set = [416,640,768,960,1280,1920]
e_height_set = [234,360,432,540,720,1080]

plt.figure()
plt.figure(figsize=(15,95))

for i,id in enumerate(video_id):
    dataset = df.loc[df['s_video_id'] == id]
    dataset = np.array(dataset)
    
    # plot (bitrate,vmaf) points for every resolution
    plt.subplot(18,3,i+1)
    for k, width in enumerate(e_width_set):
        index = np.where(dataset[:,1]==width)
        data_resolution = dataset[index]
        
        plt.plot(data_resolution[:,-2],data_resolution[:,-1],label=f'resolution {width}x{e_height_set[k]}')
        
    # prepare points(bitrate,vmaf) in the plot
    points = dataset[:,-2:]
    
    # find the convex hull
    hull = ConvexHull(points)
    points_hull = points[hull.vertices]
    points_hull = points_hull[np.argsort(points_hull[:,0])]
    
    plt.plot(points_hull[:,0],points_hull[:,1],'-',color='darkblue',label='Convex Hull')
    
    plt.title(f'video id {id}')
    plt.xlabel('average bitrate')
    plt.ylabel('predicted VMAF')
    plt.legend()

plt.show()



