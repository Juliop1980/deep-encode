# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction import DictVectorizer

df = pd.read_csv('pse_data.csv')
dataset = df.iloc[:,:43]

#unimportant features, small amount of values: s_scan_type,c_content_category,c_colorhistogram_temporal_mean_std_dev_dark,
#c_colorhistogram_temporal_mean_std_dev_medium_dark,
#c_colorhistogram_temporal_mean_std_dev_medium_bright,c_colorhistogram_temporal_mean_std_dev_bright
dataset = dataset.drop(columns=['c_content_category','c_colorhistogram_temporal_mean_std_dev_dark',
                                'c_colorhistogram_temporal_mean_std_dev_medium_dark',
                                'c_colorhistogram_temporal_mean_std_dev_medium_bright',
                                'c_colorhistogram_temporal_mean_std_dev_bright'])

#constant features:s_scan_type,s_height,c_scene_change_py_thresh30,c_scene_change_py_thresh50,e_aspect_ratio,
# e_pixel_aspect_ratio,e_codec,e_b_frame_int,e_ref_frame_count,e_bit_depth,e_pixel_fmt
dataset = dataset.drop(columns=['s_scan_type','s_height','c_scene_change_py_thresh30','c_scene_change_py_thresh50',
                                'e_aspect_ratio','e_pixel_aspect_ratio','e_codec',
                                'e_b_frame_int','e_ref_frame_count','e_bit_depth','e_pixel_fmt'])


#a few unknown values in:e_codec_profile (not number)
dataset_codec_profile = df[['e_codec_profile','t_average_vmaf']]
dataset_codec_profile= dataset_codec_profile.loc[dataset_codec_profile['e_codec_profile'] != 'unknown']

#many unknown values in:e_scan_type (not number)
dataset_e_scan_type = df[['e_scan_type','t_average_vmaf']]
dataset_e_scan_type= dataset_e_scan_type.loc[dataset_e_scan_type['e_scan_type'] != 'unknown']

dataset_c_content_category =  df[['c_content_category','t_average_vmaf']]
dataset_c_content_category =  dataset_c_content_category.loc[dataset_c_content_category['c_content_category'] != '']
#print(dataset_codec_profile)

#cor_matrix has no 'e_codec_profile','e_scan_type' columns
cor_matrix = dataset.corr()
correlation = cor_matrix[['t_average_vmaf']]
print(correlation)

# e_crf, e_width, e_height, e_codec_level, t_average_bitrate, t_average_vmaf have much impact on VMAF
# t_average_bitrate has greater impact on vmaf
print(correlation.loc[abs(correlation['t_average_vmaf']) >=0.1 ])

# category -> numeric
dict_vec = DictVectorizer(sparse=False)
dataset_codec_profile = dict_vec.fit_transform(dataset_codec_profile.to_dict('records'))
dataset_codec_profile = pd.DataFrame(dataset_codec_profile)

#e_codec_profile has impact on vmaf, the last column present the correlation of e_codec_profile and vmaf
print(dataset_codec_profile.corr()) 

# category -> numeric
dataset_e_scan_type = dict_vec.fit_transform(dataset_e_scan_type.to_dict('records'))
dataset_e_scan_type = pd.DataFrame(dataset_e_scan_type)
# e_scan_type has very small impact on vmaf
print(dataset_e_scan_type.corr())

# c_content_category has very small impact on vmaf
dataset_c_content_category = dict_vec.fit_transform(dataset_c_content_category.to_dict('records'))
dataset_c_content_category = pd.DataFrame(dataset_c_content_category)
print(dataset_c_content_category.corr())

#remove the unknown values from e_codec_profile
dataset= dataset.loc[dataset['e_codec_profile'] != 'unknown']

#choose attributes: e_crf, e_width, e_height,e_codec_profile, e_codec_level,t_average_bitrate, t_average_vmaf
dataset = dataset[['s_video_id','e_crf','e_width', 'e_height','e_codec_profile','e_codec_level','t_average_bitrate', 't_average_vmaf']]



