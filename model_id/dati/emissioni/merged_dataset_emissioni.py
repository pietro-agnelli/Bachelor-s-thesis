# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 10:31:35 2023

@author: Pietro
"""
import os
import pandas as pd

name_folds = ['NH3' ,'NOx','PM10']
name_files_id = ['2013','2014','2015','2016','2017','2018']
name_files_val = ['2019','2020','2021']
dataset_emissioni_id = pd.DataFrame()
dataset_emissioni_val = pd.DataFrame()
#files = os.listdir(name_fold)
for fold in range (len(name_folds)):
    for nf in range(len(name_files_id)):
        df_emissioni = pd.read_csv(name_folds[fold] + '/' + name_files_id[nf]+'.csv')
        df_emissioni.drop(df_emissioni.columns[0], axis = 1, inplace = True)
        dataset_emissioni_id = pd.concat([dataset_emissioni_id, df_emissioni],ignore_index=True)
    dataset_emissioni_id.to_csv('dataset_emissioni_id_' + name_folds[fold]+ '.csv', index=False)
    dataset_emissioni_id = pd.DataFrame()
 
for folds in range(len(name_folds)):
   for nf in range(len(name_files_val)):
       df_emissioni = pd.read_csv(name_folds[folds] + '/' + name_files_val[nf]+'.csv')
       df_emissioni.drop(df_emissioni.columns[0], axis = 1, inplace = True)
       dataset_emissioni_val = pd.concat([dataset_emissioni_val, df_emissioni],ignore_index=True)
   dataset_emissioni_val.to_csv('dataset_emissioni_val_' +name_folds[folds]+'.csv', index=False)
   dataset_emissioni_val = pd.DataFrame()
   
   
# name_files_merged=['dataset_NH3' 'dataset_NOx' 'dataset_PM10']
# for nf in range(len(name_files_merged)):
#     df_emissioni = pd.read_csv('emissioni/' + name_files_id[nf]+'.csv')
#     df_emissioni.drop(df_emissioni.columns[0], axis = 1, inplace = True)
#     dataset_emissioni_id_v2 = pd.concat([dataset_emissioni_id, df_emissioni],ignore_index=True)
#     dataset_emissioni_id_v2.to_csv('dataset_emissioni_id.csv', index=False)


identification = ['dataset_emissioni_id_NH3','dataset_emissioni_id_NOx','dataset_emissioni_id_PM10']
validation = ['dataset_emissioni_val_NH3','dataset_emissioni_val_NOx','dataset_emissioni_val_PM10']
dataset_emissioni_id_finale=pd.DataFrame()
for idx in range(len(identification)):
   df_emissioni = pd.read_csv( identification[idx]+'.csv')
   dataset_emissioni_id_finale = pd.concat([dataset_emissioni_id_finale, df_emissioni],axis=1)
dataset_emissioni_id_finale.to_csv('dataset_emissioni_id_finale.csv', index=False)

dataset_emissioni_val_finale=pd.DataFrame()
for idx in range(len(identification)):
   df_emissioni = pd.read_csv( validation[idx]+'.csv')
   dataset_emissioni_val_finale = pd.concat([dataset_emissioni_val_finale, df_emissioni],axis=1)
dataset_emissioni_val_finale.to_csv('dataset_emissioni_val_finale.csv', index=False)



                  
#pulisco i dataset e li unisco
# df = pd.DataFrame()
# for index in range(len(name_folds)):
#     ex = pd.read_csv('dataset_'+name_folds[index]+'.csv')
#     df = pd.concat([df, ex], axis = 1)

# df.drop(df.columns[0], axis = 1, inplace = True)
# df.to_csv('dataset_emissioni.csv', index=False)