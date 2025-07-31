#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 14:42:21 2023

@author: claudio
"""
import numpy as np
# def trasla(na,nb,nk,len_dataset):

# 	# riceve in ingresso il termine na e i due vettori nb e nk (vanno passati come vettori anche se hanno 1 elemento solo).
# 	# riceve inoltre due vettori y e u, che sono i dati che abbiamo relativi rispettivamente all'input e all'output.
# 	# resituisce due elementi numpy: la matrice M e il vettore teta
# 	# procediamo subito a convertire tutti i vettori in array di numpy
# 	min_u=0
# 	min_a=0
# 	
# 	if na>0:
# 		inizio_ar=np.array(range(0,-na,-1))-1
# 		min_a=np.min(inizio_ar)
# 	else:
# 		inizio_ar=[]

# 	if type(nb) is int:
# 		if nb>0:
# 			num_ex=1
# 			inizio_ex=0
# 		else:
# 			num_ex=0
# 			inizio_ex=[]
# 	else:
# 		num_ex=len(nb)
# 		inizio_ex=np.full([num_ex,np.max(nb)],np.nan)
# 	for i in range(0,num_ex):
# 		if type(nb) is int:
# 			max_ord=nb
# 			max_del=nk
# 		else:
# 			max_ord=nb[i]
# 			max_del=nk[i]
# 		
# 		inizio_ex[i,0:max_ord]=np.array(range(0-max_del,-max_ord-max_del,-1))
# 		
# 		min_u=np.nanmin(inizio_ex)
# 	
# 	minimo=np.min([min_a,min_u])
# 	print(minimo)
# 	if len(inizio_ar):
# 		inizio_ar_traslato=inizio_ar-minimo
# 	else:
# 		inizio_ar_traslato=[]

# 	if len(inizio_ex):
# 		inizio_ex_traslato=inizio_ex-minimo
# 	else:
# 		inizio_ex_traslato=[]
# 	
# 	inizio_out=0
# 	inizio_out_traslato=-minimo
# 	
# 	print(inizio_out)
# 	print(inizio_ar)
# 	print(inizio_ex)
# 	print(inizio_out_traslato)
# 	print(inizio_ar_traslato)
# 	print(inizio_ex_traslato)
# 	return(inizio_out,inizio_ar,inizio_ex,inizio_out_traslato,inizio_ar_traslato,inizio_ex_traslato)
# 		
def start_shift(na,nb,nk):

	# riceve in ingresso il termine na e i due vettori nb e nk (vanno passati come vettori anche se hanno 1 elemento solo).
	# riceve inoltre due vettori y e u, che sono i dati che abbiamo relativi rispettivamente all'input e all'output.
	# resituisce due elementi numpy: la matrice M e il vettore teta
	# procediamo subito a convertire tutti i vettori in array di numpy
	min_u=0
	min_a=0
	
	if na>0:
		inizio_ar=np.array(range(0,-na,-1))-1
		min_a=np.min(inizio_ar)
	else:
		inizio_ar=[]

	if type(nb) is int:
		nb=np.append(nb,np.nan)
		nk=np.append(nk,np.nan)
		num_ex=1
	else:
		num_ex=len(nb)
	
	if len(nb)==0 or np.nanmax(nb)<=0:
		inizio_ex=[]
	else:
		inizio_ex=np.full([num_ex,int(np.nanmax(nb))],np.nan)
		for i in range(0,num_ex):
			max_ord=int(nb[i])
			max_del=int(nk[i])
			inizio_ex[i,0:max_ord]=np.array(range(0-max_del,-max_ord-max_del,-1))
		min_u=np.nanmin(inizio_ex)
		
	minimo=np.min([min_a,min_u])
	if len(inizio_ar):
		inizio_ar_traslato=inizio_ar-minimo
	else:
		inizio_ar_traslato=[]

	if len(inizio_ex):
		inizio_ex_traslato=inizio_ex-minimo
	else:
		inizio_ex_traslato=[]
	
	inizio_out=0
	inizio_out_traslato=-minimo
	
	return(inizio_out,inizio_ar,inizio_ex,inizio_out_traslato,inizio_ar_traslato,inizio_ex_traslato)

def clean (y,X):
	
	S=np.sum(X,axis=1)
	bad=np.isnan(S)
	X=np.delete(X,bad,axis=0)
	y=np.delete(y,bad)
	bad=np.isnan(y)
	X=np.delete(X,bad,axis=0)
	y=np.delete(y,bad)
	return (y,X)

def dataset_shift (y,U,na,nb,nk):
	inizio_out,inizio_ar,inizio_ex,inizio_out_traslato,inizio_ar_traslato,inizio_ex_traslato=start_shift(na,nb,nk)
	yout=y[int(inizio_out_traslato):]
	L=len(yout)
	X=np.zeros([L,na+np.sum(nb)])
	cont=0
	if len(inizio_ex_traslato):
		for i in range(len(nb)):
			for j in range(nb[i]):
				X[:,cont]=U[int(inizio_ex_traslato[i,j]):int(inizio_ex_traslato[i,j])+L,i].flatten()
				cont=cont+1

	if len(inizio_ar_traslato):
		for j in range(na):
			X[:,cont]=y[int(inizio_ar_traslato[j]):int(inizio_ar_traslato[j]+L)]
			cont=cont+1

	X=np.array(X)
	return(yout,X)

'''
il metodo valid_perf fornisce in unscita un vettore contente tutte le metriche di accuratezza della previsione
'''
def valid_perf(y_true,y_pred):
	import sklearn.metrics as mt
	r2=mt.r2_score(y_true, y_pred)
	me=np.average(y_true-y_pred)
	nme=me/np.average(y_true)
	mae=mt.mean_absolute_error(y_true, y_pred)
	mse=mt.mean_squared_error(y_true, y_pred)
	#msle=mt.mean_squared_log_error(y_true, y_pred)
	mape=mt.mean_absolute_percentage_error(y_true, y_pred)
	nmae=mae/np.average((np.abs(y_true)))
	medae=mt.median_absolute_error(y_true, y_pred)
	maxe=mt.max_error(y_true, y_pred)
	evar=mt.explained_variance_score(y_true, y_pred)
	perf_dict={}
	for variable in ["r2","me","nme","mae","mse","mape","nmae","medae","maxe","evar"]:
		perf_dict[variable] = eval(variable)
	
	return(perf_dict)

def nanpredict(model,X):
	L=np.size(X,axis=0)
	print(L)
	y=np.zeros([L])
	for i in range(0,L):
		S=np.sum(X[i,:])
		bad=np.isnan(S)
		
		if bad:
			y[i]=np.nan
		else:
			input=np.reshape(X[i,:],[1,-1])
			y[i]=model.predict(input)
	
	return y	
		
		
def accuracy(confusion_matrix):
   diagonal_sum = confusion_matrix.trace()
   sum_of_all_elements = confusion_matrix.sum()
   return diagonal_sum / sum_of_all_elements
		
#------------------------------------------------------------------------------
def write_perf_models(dict_models,fileout,perf_idx):
    import pandas as pd
    import numpy as np

    df=pd.DataFrame.from_dict(dict_models)
    perf=df[perf_idx]

    print(perf)
    print(type(perf[0]))
    chiavi=list(perf[0].keys())
    num_model=len(perf)
    matrice=np.zeros([num_model,len(chiavi)])
    for i in range(0,len(perf)):
        j=0
        for item in chiavi:
            matrice[i,j]=perf[i][item]
            j=j+1
    perf_out=pd.DataFrame(matrice,index=df["name"],columns=chiavi)
    print(fileout)
    perf_out.to_csv(fileout)

		
		
		
#------------------------------------------------------------------------------
