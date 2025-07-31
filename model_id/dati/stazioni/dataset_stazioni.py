# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 10:53:48 2023

@author: Pietro
"""
import os
import pandas as pd

name_folds = ['IT1734A' , 'IT2072A']
name_files_id = ['2013','2014','2015','2016','2017','2018']
name_files_val = ['2019','2020','2021']

dataset = pd.DataFrame()

for fold_index in range(len(name_folds)):
    for index in range(len(name_files_id)):
        df_stazioni = pd.read_csv(name_folds[fold_index] + '/' + name_files_id[index]+'.csv')
        df_stazioni.drop(df_stazioni.columns[0:4], axis = 1, inplace = True)
        dataset = pd.concat([dataset, df_stazioni], ignore_index=True)
    dataset.to_csv('dataset_' + name_folds[fold_index] +'_id.csv')
    dataset = pd.DataFrame()

for fold_index in range(len(name_folds)):
    for index in range(len(name_files_val)):
        df_stazioni = pd.read_csv(name_folds[fold_index] + '/' + name_files_val[index]+'.csv')
        df_stazioni.drop(df_stazioni.columns[0:4], axis = 1, inplace = True)
        dataset = pd.concat([dataset, df_stazioni], ignore_index=True)
    dataset.to_csv('dataset_' + name_folds[fold_index] +'_val.csv')
    dataset = pd.DataFrame()
# name_fold = 'PM10'
# name_files_id = ['2013','2014','2015','2016','2017','2018']
# name_files_val = ['2019','2020','2021']
# dataset_emissioni_id = pd.DataFrame()
# dataset_emissioni_val = pd.DataFrame()
# #files = os.listdir(name_fold)
# for nf in range(len(name_files_id)):
#    df_emissioni = pd.read_csv(name_fold + '/' + name_files_id[nf]+'.csv')
#    df_emissioni.drop(df_emissioni.columns[0], axis = 1, inplace = True)
#    dataset_emissioni_id = pd.concat([dataset_emissioni_id, df_emissioni],axis = 1)
#    dataset_emissioni_id.to_csv('dataset_emissioni_id.csv', index=False)
   
   
# for nf in range(len(name_files_val)):
#    df_emissioni = pd.read_csv(name_fold + '/' + name_files_val[nf]+'.csv')
#    df_emissioni.drop(df_emissioni.columns[0], axis = 1, inplace = True)
#    dataset_emissioni_val = pd.concat([dataset_emissioni_val, df_emissioni],axis = 1)
#    dataset_emissioni_val.to_csv('dataset_emissioni_val.csv', index=False)
                   
#pulisco i dataset e li unisco
# df = pd.DataFrame()
# for index in range(len(name_folds)):
#     ex = pd.read_csv('dataset_'+name_folds[index]+'.csv')
#     df = pd.concat([df, ex], axis = 1)

# df.drop(df.columns[0], axis = 1, inplace = True)
# df.to_csv('dataset_emissioni.csv', index=False)
