# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('pse_data.csv')

# choose attributes:s_video_id, e_crf , e_width, e_height,e_codec_profile, e_codec_level,t_average_bitrate,t_average_vmaf
dataset = df[['s_video_id','e_crf','e_width', 'e_height','e_codec_profile','e_codec_level',
              't_average_bitrate', 't_average_vmaf']]
data= dataset.loc[dataset['e_codec_profile'] != 'unknown']
# save the cleaned data
#dataset.to_csv("cleaned_data.csv")

# [e_codec_level,e_codec_profile(high=1),e_codec_profile(main=1),e_crf,e_height,e_width,t_average_bitrate,t_average_vmaf]
dict_vec = DictVectorizer(sparse=False)
cleaned_data = dict_vec.fit_transform(data.to_dict('records'))

#split train set and test set, the last column is vmaf
X_train,X_test,y_train,y_test = train_test_split(cleaned_data[:,:-1],cleaned_data[:,-1],
                                                 test_size=0.25,random_state=0)

# select appropriate parameters
# max_depth refers to the number of leaves of each tree
def test_GradientBoostingRegressor_maxdepth(*data):
    '''
    test the impact of max_depth on GradientBoostingRegressor
    '''
    X_train,X_test,y_train,y_test=data
    maxdepths=np.arange(1,20)
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    testing_scores=[]
    training_scores=[]
    for maxdepth in maxdepths:
        regr=ensemble.GradientBoostingRegressor(max_depth=maxdepth,max_leaf_nodes=None)
        regr.fit(X_train,y_train)
        training_scores.append(regr.score(X_train,y_train))
        testing_scores.append(regr.score(X_test,y_test))
    ax.plot(maxdepths,training_scores,label="Training Score")
    ax.plot(maxdepths,testing_scores,label="Testing Score")
    ax.set_xlabel("max_depth")
    ax.set_ylabel("score")
    ax.legend(loc="lower right")
    ax.set_ylim(-1,1.05)
    plt.suptitle("GradientBoostingRegressor")
    plt.show()


# n_estimators refers to the total number of trees in the ensemble
def test_GradientBoostingRegressor_num(*data):
    '''
    test the impact of n_estimators on GradientBoostingRegressor
    '''
    X_train,X_test,y_train,y_test=data
    nums=np.arange(1,500,step=2)
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    testing_scores=[]
    training_scores=[]
    for num in nums:
        regr=ensemble.GradientBoostingRegressor(n_estimators=num)
        regr.fit(X_train,y_train)
        training_scores.append(regr.score(X_train,y_train))
        testing_scores.append(regr.score(X_test,y_test))
    ax.plot(nums,training_scores,label="Training Score")
    ax.plot(nums,testing_scores,label="Testing Score")
    ax.set_xlabel("estimator num")
    ax.set_ylabel("score")
    ax.legend(loc="lower right")
    ax.set_ylim(0,1.05)
    plt.suptitle("GradientBoostingRegressor")
    plt.show()
    
 
def test_GradientBoostingRegressor_learning(*data):
    '''
    test the impact of learning_rate on GradientBoostingRegressor
    '''
    X_train,X_test,y_train,y_test=data
    learnings=np.linspace(0.01,1.0)
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    testing_scores=[]
    training_scores=[]
    for learning in learnings:
        regr=ensemble.GradientBoostingRegressor(learning_rate=learning)
        regr.fit(X_train,y_train)
        training_scores.append(regr.score(X_train,y_train))
        testing_scores.append(regr.score(X_test,y_test))
    ax.plot(learnings,training_scores,label="Training Score")
    ax.plot(learnings,testing_scores,label="Testing Score")
    ax.set_xlabel("learning_rate")
    ax.set_ylabel("score")
    ax.legend(loc="lower right")
    ax.set_ylim(-1,1.05)
    plt.suptitle("GradientBoostingRegressor")
    plt.show()
    
# plot the relation between the parameters and the scores
    
test_GradientBoostingRegressor_maxdepth(X_train,X_test,y_train,y_test)
test_GradientBoostingRegressor_num(X_train,X_test,y_train,y_test)    
test_GradientBoostingRegressor_learning(X_train,X_test,y_train,y_test)


# choose max_depth = 4, n_estimators = 500, learning_rate = 0.1
best_regressor = ensemble.GradientBoostingRegressor(
    max_depth=4,
    n_estimators=500,
    learning_rate=0.1
)
best_regressor.fit(X_train, y_train)

y_pred = best_regressor.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
score = best_regressor.score(X_test,y_test)
print(mae,score)


# predict the whole dataset
y_pred_all = best_regressor.predict(cleaned_data[:,:8])

def getAllPrediction(data,y_pred_all) :

    prediction = np.concatenate((np.array(data[['s_video_id']]).reshape(len(y_pred_all),1),
                                 np.array(data[['e_width']]).reshape(len(y_pred_all),1),
                                 np.array(data[['e_height']]).reshape(len(y_pred_all),1),
                                 np.array(data[['t_average_bitrate']]).reshape(len(y_pred_all),1),
                                 y_pred_all.reshape(len(y_pred_all),1)),axis=1)
    df_prediction = pd.DataFrame(prediction)
    df_prediction.columns=['s_video_id','e_width', 'e_height','t_average_bitrate', 'predicted_vmaf']

    return df_prediction
   
df_prediction = getAllPrediction(data, y_pred_all)

# save the predicted values    
#df_prediction.to_csv("predicted_vmaf.csv",index=0)
    




