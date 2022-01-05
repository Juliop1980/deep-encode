import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from scipy.spatial import ConvexHull

# read file and prepare dataset
df = pd.read_csv('pse_data.csv')
df = df.iloc[:,:43]
#s_storage_size/s_duration 
#c_si  -0.051523, e_framerate   -0.043234, e_gop_size  -0.043234
df_data = df[['s_video_id','c_si','e_framerate','e_gop_size','e_crf','e_width', 'e_height','e_codec_profile','e_codec_level',
                   't_average_bitrate', 't_average_vmaf']]
df_data= df_data.loc[df_data['e_codec_profile'] != 'unknown']

video_id = np.unique(np.array(df_data[['s_video_id']]))
#print(len(video_id))

e_width_set = [416,640,768,960,1280,1920]
e_height_set = [234,360,432,540,720,1080]

mae_set =[]
score_set =[]
bitrate_ladder = pd.DataFrame()

def obtainDatasetId(df_data,id):
    dataset= df_data.loc[df_data['s_video_id'] == id]
    dataset= dataset[['e_crf','e_width', 'e_height','e_codec_profile','e_codec_level',
                      't_average_bitrate', 't_average_vmaf']]
    
    # column of the data
    # [e_codec_level,e_codec_profile(high=1),e_codec_profile(main=1),e_crf,e_height,e_width,t_average_bitrate,t_average_vmaf]
    dict_vec = DictVectorizer(sparse=False)
    data_id = dict_vec.fit_transform(dataset.to_dict(orient='record'))
    m,n = data_id.shape
    X_train,X_test,y_train,y_test = train_test_split(data_id[:,:n-1],data_id[:,n-1],test_size=0.25,random_state=0)
    
    return m,n,data_id,X_train,X_test,y_train,y_test


plt.figure()
plt.figure(figsize=(15,95))
for i,id in enumerate(video_id):
    m,n,data,X_train,X_test,y_train,y_test = obtainDatasetId(df_data, id)
       
    regr = ensemble.GradientBoostingRegressor(
            max_depth=2,
            learning_rate=0.1,
            n_estimators=500
            )
    model = regr.fit(X_train,y_train)
    
    # evaluate the model
    y_pred_test = regr.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred_test)
    score = regr.score(X_test,y_test)
    mae_set.append(mae)
    score_set.append(score)
    
    # predict the whole dataset
    y_pred_all = regr.predict(data[:,:n-1])
    
    plt.subplot(18,3,i+1)
    for k, width in enumerate(e_width_set):
        index = np.where(data[:,5]==width)
        data_resolution = data[index]
        y_pred = y_pred_all[index]
        
        plt.plot(data_resolution[:,n-2],y_pred,label=f'resolution {width}x{e_height_set[k]}')
    
    # prepare points(bitrate,vmaf) in the plot
    points = np.concatenate((data[:,n-2].reshape(len(y_pred_all),1),y_pred_all.reshape(len(y_pred_all),1)),axis=1)
    
    hull = ConvexHull(points)
    points_hull = points[hull.vertices]
    points_hull = points_hull[np.argsort(points_hull[:,0])]
    
    plt.plot(points_hull[:,0],points_hull[:,1],'-',color='darkblue',label='Convex Hull')
    
    plt.title(f'video id {id}')
    plt.xlabel('average bitrate')
    plt.ylabel('average vmaf')
    plt.legend()
    
    # datapoints on the convexhull [width,bitrate,vmaf]
    ladder_height = data[hull.vertices,4]
    ladder_width = data[hull.vertices,5]
    ladder_bitrate = data[hull.vertices,6]
    ladder_vmaf = data[hull.vertices,7]
    ladder_temp = np.concatenate((ladder_width.reshape(len(ladder_height),1),ladder_height.reshape(len(ladder_height),1),ladder_bitrate.reshape(len(ladder_height),1),
                                  ladder_vmaf.reshape(len(ladder_height),1)),axis=1)
    
    '''
    # for the same resolution, select the ladder with lower bitrate
    ladder1 = np.zeros((len(np.unique(ladder_temp[:,0])),3))
    for i,value in enumerate(np.unique(ladder_temp[:,0])):
        arg1 = np.where(ladder_temp[:,0]==value)
        ladder_resolution = ladder_temp[arg1]
        arg2 = np.where(ladder_temp[:,1]==np.max(ladder_resolution[:,1]))
        ladder1[i,:] = ladder_temp[arg2]
    ladder_int = np.round(ladder1).astype(int)
    print('Video ID',id,'\n',ladder_int)
    '''
    
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
    #print(ladder)
    
    ladder.drop(index=(ladder.loc[ladder['VMAF']<10].index),inplace=True)
    
    if i == 0:
        bitrate_ladder = ladder
    else:
        bitrate_ladder = bitrate_ladder.append(ladder,ignore_index=True)

#bitrate_ladder.to_excel("bitrate_ladder.xlsx",index=False)      
plt.show()
print('MAE:',np.mean(mae_set),'score:',np.mean(score_set))