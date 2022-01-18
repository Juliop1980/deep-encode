# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull

df = pd.read_csv('predicted_vmaf.csv')

video_id = np.unique(np.array(df[['s_video_id']]))
e_width_set = [416,640,768,960,1280,1920]
e_height_set = [234,360,432,540,720,1080]

bitrate_ladder = pd.DataFrame()

for i,id in enumerate(video_id):
    dataset = df.loc[df['s_video_id'] == id]
    dataset = np.array(dataset)
        
    # prepare points(bitrate,vmaf)
    points = dataset[:,-2:]
    
    # find the convex hull
    hull = ConvexHull(points)
    points_hull = points[hull.vertices]
    
    # datapoints on the convexhull [width,height,bitrate,vmaf]
    ladder_width = dataset[hull.vertices,1]
    ladder_height = dataset[hull.vertices,2]
    ladder_temp = np.concatenate((ladder_width.reshape(len(ladder_height),1),
                                  ladder_height.reshape(len(ladder_height),1),
                                  points_hull),axis=1)
    
    # select bitrate around 300，400，700，1000，1500, 2000
    # classify the points on covex hull by bitrate smaller than 350，450，750，1050，1550
    ladder = []
    ladder_350= []
    ladder_450= []
    ladder_750= []
    ladder_1050= []
    ladder_1550= []
    ladder_2550 = []
    
    ladder_temp = np.round(ladder_temp).astype(int)
    for i,bit in enumerate(ladder_temp[:,2]):
        if  bit < 350:
            ladder_350.append(ladder_temp[i])
        elif (bit >= 350 and bit < 450):
            ladder_450.append(ladder_temp[i])        
        elif (bit >= 450 and bit < 750):
            ladder_750.append(ladder_temp[i])        
        elif (bit >= 750 and bit < 1050):
            ladder_1050.append(ladder_temp[i])
        elif (bit >= 1050 and bit < 1550):
            ladder_1550.append(ladder_temp[i])
        elif (bit >= 1550 and bit < 2550):
            ladder_2550.append(ladder_temp[i])
    
    # select bitrate around 300，400，700，1000，1500
    if len(ladder_350)!=0:
        ladder.append(ladder_350[-1])
    if len(ladder_450)!=0: 
        ladder.append(ladder_450[-1])
    if len(ladder_750)!=0:
        ladder.append(ladder_750[-1])
    if len(ladder_1050)!=0:
        ladder.append(ladder_1050[-1])
    if len(ladder_1550)!=0:
        ladder.append(ladder_1550[-1])
    if len(ladder_2550)!=0:
        ladder.append(ladder_2550[-1])
        
    ladder = np.array(ladder)
    ladder = pd.DataFrame(ladder)
    ladder.columns=['resolution width','resolution height','bitrate','VMAF']
    ladder['video ID'] = id
    ladder= ladder[['video ID','resolution width','resolution height','bitrate','VMAF']]
    
    # drop the bitrate/vmaf pairs with very low vmaf value
    ladder.drop(index=(ladder.loc[ladder['VMAF']<10].index),inplace=True)
    
    if i == 0:
        bitrate_ladder = ladder
    else:
        bitrate_ladder = bitrate_ladder.append(ladder,ignore_index=True)
        
#bitrate_ladder.to_excel("bitrate_ladder.xlsx",index=False)
    
    
    
    
    
