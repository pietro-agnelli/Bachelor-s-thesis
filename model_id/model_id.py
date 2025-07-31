    #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import sklearn.metrics as sk_score
from arx_utils import dataset_shift, clean, valid_perf, nanpredict, write_perf_models
from utility import leggi_conf, clear
from utility import leggi_csv, leggi_xlsx
import joblib as jbl
import os
import sys
import seaborn as sns

err,name_test,name_y_file_train,name_y_file_val, name_u_file_train, name_u_file_val,name_out_file, colX, colY, colU, ar_ord,ex_ord,ex_del=leggi_conf()

if err:
	sys.exit(1)

path_out='./'+name_test
if not(os.path.isdir(path_out)):
	os.mkdir(path_out)


###############################################################################
#SCOMPOSIZIONE DATAFRAME IN VALIDATION-TRAIN VALUE
#divido il dataframe in sezioni train e validation
yT_train=leggi_csv(name_y_file_train)
yV_train=np.array(yT_train.iloc[:,colY])#estraggo la colonna riferita ai valori di concentrazione di pm10 dal file IT0187A_PM10_day.xlsx

uT_train=leggi_csv(name_u_file_train)
uV_train=np.matrix(uT_train.iloc[:,colU])#creo una matrice con i valori di tempmin e temp che userò come dati di allenamento 

yT_val=leggi_csv(name_y_file_val)
yV_val=np.array(yT_val.iloc[:,colY])

uT_val=leggi_csv(name_u_file_val)
uV_val=np.matrix(uT_val.iloc[:,colU])


# p = figure(title="Simple line example", x_axis_lab2el='x', y_axis_label='y')
# # add a line renderer with legend and line thickness to the plot
# x=np.array(range(0,len(yV)))
# p.line(x,uV[:,0], legend_label="Temp.", line_wtrainth=2)
# show(p)

#ar_ord : ordine parte regressiva 
#ex_ord : ordine parte esogena
#ex_del : delay parte esogena
y_train,X_train=dataset_shift(yV_train,uV_train, ar_ord,ex_ord,ex_del) 
y_train_clean, X_train_clean=clean(y_train,X_train)
y_val,X_val=dataset_shift(yV_val,uV_val,ar_ord,ex_ord,ex_del)
y_val_clean, X_val_clean=clean(y_val,X_val)
# list of models
models=[]

#salvo il dataset su cui devo eseguire le regressio
arx= pd.DataFrame(X_train_clean)
arx.to_csv('arx.csv')

#i due vettori/matrici train/validation devono essere diversi, lo verifico:
#print(np.allclose(y_train_clean, y_val_clean))

###############################################################################
# Linear Regression model
model=LinearRegression()
model.fit(X_train_clean,y_train_clean)   #fit è un metodo che divtraine tutti i valori/ la media di ogni valore per il massimo di quella categoria, cosi facendo tutti i valori sono allo stesso livello : normalizzazione?
ypred_train_clean=model.predict(X_train_clean)
ypred_val_clean=model.predict(X_val_clean)
perf_train=valid_perf(y_train_clean,ypred_train_clean)
perf_val=valid_perf(y_val_clean,ypred_val_clean)
y_pred_val=nanpredict(model,X_val)
y_pred_train=nanpredict(model,X_train)
model_d=dict(name='LR',model=model,perf_train=perf_train, perf_val=perf_val, ar_ord=ar_ord, ex_ord=ex_ord, ex_del=ex_del, X_train=X_train, X_train_clean=X_train_clean, y_train=y_train, y_train_clean=y_train_clean, X_val=X_val, X_val_clean=X_val_clean, y_val=y_val, y_val_clean=y_val_clean)
models.append(model_d)



###############################################################################
#NEURAL NETWORK MODEL
from sklearn.neural_network import MLPRegressor
#opt = SGDClassifier(learning_rate=0.1) 


#Problema: il vettore dei valori_pred contiene sempre lo stesso numero, possibile soluzione normalizzare il dataset
from sklearn import preprocessing
# X_train_clean_nn = preprocessing.normalize(X_train_clean, norm='max')
# y_train_clean_nn = preprocessing.normalize([y_train_clean], norm = 'max')
# y_train_clean_nn = np.transpose(y_train_clean_nn)
# X_val_clean_nn = preprocessing.normalize(X_val_clean, norm = 'max')
# y_val_clean_nn = preprocessing.normalize([y_val_clean], norm = 'max')
# y_val_clean_nn = np.transpose(y_val_clean_nn)
#
#Max = np.maximum.reduce(pd.concat([X_train_clean, y_train_clean, X_val_clean,y_val_clean]), axis = 1)
Max = max(X_train_clean.flatten())
X_train_clean_nn =X_train_clean/Max 
y_train_clean_nn = y_train_clean/Max
y_train_clean_nn = np.transpose(y_train_clean_nn)
X_val_clean_nn = X_val_clean/Max
y_val_clean_nn = y_val_clean/Max
y_val_clean_nn = np.transpose(y_val_clean_nn)

#partire con un hidden layer
#activation function n ingressi , neuroni nell hl n/2 a 20n
model_nn = MLPRegressor( hidden_layer_sizes=(20,5) , max_iter=100, activation='tanh', learning_rate_init=0.01).fit(X_train_clean_nn, y_train_clean_nn) #alleno la rete neurale
ypred_train_clean_nn = model_nn.predict(X_train_clean_nn)
ypred_train_clean_nn = ypred_train_clean_nn*Max
ypred_val_clean_nn = model_nn.predict(X_val_clean_nn)
ypred_val_clean_nn = ypred_val_clean_nn*Max
perf_train_nn=valid_perf(y_train_clean,ypred_train_clean_nn)
perf_val_nn=valid_perf(y_val_clean,ypred_val_clean_nn)
y_pred_val_nn=nanpredict(model_nn,X_val_clean_nn)
y_pred_train_nn=nanpredict(model_nn,X_train_clean_nn)


#NB: il predicting fatto sui valori di train oltre quelli di validation viene fatto
#perchè se le prestazioni sulle validation non sono alte, non necessariamente
#la rete neurale è troppo semplice (tratta i dati in modo approssimativo),
#se le prestazioni sui train sono troppo alte si può incorrere in overfitting

model__NN=dict(name='NN',model=model_nn,perf_train=perf_train_nn, perf_val=perf_val_nn, ar_ord=ar_ord, ex_ord=ex_ord, ex_del=ex_del, X_train=X_train, X_train_clean=X_train_clean_nn, y_train=y_train, y_train_clean=y_train_clean_nn, X_val=X_val, X_val_clean=X_val_clean_nn, y_val=y_val, y_val_clean=y_val_clean_nn)
models.append(model__NN)



###############################################################################
# SALAVATAGGIO MODELLO E PRESTAZIONI

jbl.dump(models,path_out+'/'+'LR'+'_'+name_test+'.sav')
# LR_model=jbl.load('LR.sav')
# fine salvataggio modello

# p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')
# # # add a line renderer with legend and line thickness to the plot
# x=np.array(range(0,len(ypred)))
# p.line(x,X[:,7],legend_label="Delta", line_wtrainth=2)
# show(p)

# p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')
# # # add a line renderer with legend and line thickness to the plot
# x=np.array(range(0,len(ypred)))
# p.line(x,yout,legend_label="Delta", line_wtrainth=2)
# # show(p)


# write_perf_models(models,path_out+'/'+'perf_id.csv','perf_id')
# write_perf_models(models,path_out+'/'+'perf_val.csv','perf_val')

	
	
	
	