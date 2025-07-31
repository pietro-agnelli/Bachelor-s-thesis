#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def leggi_conf():
	err=False
	f_conf=open('conf.txt','r')
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	name_test=line.strip()
	print('Nome del test: '+name_test)
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	name_y_file_id=line.strip()
	print('Nome file y identificazione: '+ name_y_file_id)
	line=f_conf.readline()
	line=f_conf.readline()
	name_y_file_val=line.strip()
	print('Nome file y validazione: '+name_y_file_val)
	line=f_conf.readline()
	line=f_conf.readline()
	colY=int(line)
	print('Colonna dati (parte da zero): '+str(colY))
	line=f_conf.readline()
	line=f_conf.readline()
	line = line.strip() #toglie i caratteri inutili (\n etc...)
	if len(line)>0:
		colX=int(line)
		print('uhmmm'+line)
	else:
		colX=-1
			
	print('Colonna etichetta dati: '+str(colX))
	line=f_conf.readline()
	line=f_conf.readline()
	name_u_file_id=line.strip()
	print('Nome file u identificazione: '+name_u_file_id)
	line=f_conf.readline()
	line=f_conf.readline()
	name_u_file_val=line.strip()
	print('Nome file u validazione: '+name_u_file_val)
	line=f_conf.readline()
	line=f_conf.readline()
	line=line.split(',')
	line = [i.strip() for i in line] #toglie i caratteri inutili (\n etc...)
	colU=[]
	for i in range(0,len(line)):
		colU.append(int(line[i]))
	print('Colonna dati u: '+str(colU))
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	ar_ord=int(line)
	print('Ordine parte autoregressiva: '+str(ar_ord))
	line=f_conf.readline()
	line=f_conf.readline()
	line=line.split(',')
	line = [i.strip() for i in line] #toglie i caratteri inutili (\n etc...)
	ex_ord=[]
	for i in range(0,len(line)):
		ex_ord.append(int(line[i]))
	print('Ordine parte esogena: '+str(ex_ord))
	line=f_conf.readline()
	line=f_conf.readline()
	line=line.split(',')
	line = [i.strip() for i in line] #toglie i caratteri inutili (\n etc...)
	ex_del=[]
	for i in range(0,len(line)):
		ex_del.append(int(line[i]))
	print('Riatardo parte esogena: '+str(ex_del))
	line=f_conf.readline()
	line=f_conf.readline()
	line=f_conf.readline()
	name_out_file=line.strip()
	print(name_out_file)
	f_conf.close()
	
	if len(name_u_file_val)>0 and len(name_u_file_id)==0:
		print('Non è stato indicato nome file ingresso esogeno in identificazione')
		print('Il nome del file degli ingressi esogeni in validazione viene cancellato')
		name_u_file_val=[]
	
	if len(name_y_file_id)==0:
		print('Il file della variabile dipendente in identificazione deve per forza essere diverso da nullo')
		err=True
	
	if len(name_u_file_id)> 0 and len(ex_ord) != len(ex_del):
		print('i parametri di ordine e ritardo per gli ingressi esogeni devono essere in numero uguale')
		err=True
	
	return err,name_test,name_y_file_id,name_y_file_val, name_u_file_id, name_u_file_val,name_out_file, colX, colY, colU, ar_ord,ex_ord,ex_del

def leggi_csv(filename):
	import pandas as pd 
	data = pd.read_csv(filename)
	return data

def leggi_xlsx(filename):
	import pandas as pd 
	data = pd.read_excel(filename)
	return data


def clear():
	from os import system, name
# import sleep to show output for some time period 
    # for windows
	if name == 'nt':
		_ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
	else:
		_ = system('clear')




