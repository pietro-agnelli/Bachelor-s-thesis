import pandas as pd
import numpy as np
#from sklearn import linear_model

def arx(na,nb,nk,y,u): 

    # riceve in ingresso il termine na e i due vettori nb e nk (vanno passati come vettori anche se hanno 1 elemento solo). 
    # riceve inoltre due vettori y e u, che sono i dati che abbiamo relativi rispettivamente all'input e all'output.
    # resituisce due elementi numpy: la matrice M e il vettore teta
    # procediamo subito a convertire tutti i vettori in array di numpy
    y = np.array(y)
    u = np.array(u)
    if len(u.shape)==1: #controllo su u, in modo che venga trattato come matrice anche nel caso in cui sia un semplice vettore
        u = np.array([u])
    

    nb = np.array(nb)
    nk = np.array(nk)

   
    #il vettore nbk conterrà l'ampiezza di tutte le traslazioni date da nb e nk
    nbk = []

    for i in range(nb.size): #ovvero itero per un numero di volte pari alla lunghezza di nb 
        for j in range(nk[i],nb[i]+nk[i]): 
                nbk.append(j)

    nbk = np.array(nbk)

    #alcuni esempi:
    #nk=0 nb=1 --> y(t) dipende da u(t)
    #nk=1 nb=1 --> y(t) dipende da u(t-1)
    #nk=2 nb=1 --> y(t) dipende da u(t-2)
    #nk=2 nb=2 --> y(t) dipende da u(t-2) e u(t-3)

    #definiamo alcuni termini utili alla traslazione:

    if nbk.size == 0: 
        max_trasl = na
        min_trasl = 1
    else:
        na_nbk = np.concatenate(([na],nbk))
        max_trasl = max(na_nbk) # indica la massima traslazione che un vettore potrà subire.
        min_trasl = min(np.concatenate(([1],nbk))) # indica la minima traslazione che un vettore potrà subire. Se nel vettore nbk comparisse uno zero, min_trasl = 0, altrimenti
        # 1 perchè sicuramente una traslazione per y(t-1) ce l'abbiamo;
 

    len_M = y.size+min_trasl-max_trasl #e usiamo questo valore per controllare di avere abbastanza valori per la regressione richiesta:
    # infatti abbiamo problemi se questa len_M diventa 0, perchè vuole dire che la matrice M è vuota!

    if len_M>0:
               
        # ora riempiamo la matrice M con tutta la parte che riguarda y. Alla fine di questa parte, M avrà un numero di elementi pari al valore di na.
        for ar_order in range(1,na+1): # ovvero, per tutti i valori da 1 fino a na inclusi
            y_trasl = y[(max_trasl-ar_order):(len(y)-(ar_order-min_trasl))] #effettuo la traslazione di y, ottenendo y(t-1), y(t-2)...
            #print(len(y_trasl)) restituisce 1820
            if ar_order == 1:
                M = np.array([y_trasl]) #inizializzazione matrice M
                #print(M.shape) #restituisce (1, 1820, 1)
            else:
                print("ok1")
                M = np.append(M, [y_trasl], axis=0)
                #print(M.shape) restuisce (2, 1280, 1)
                #print(len([y_trasl])) restituisce 1
            

         # ora invece aggiungiamo alla matrice tutti gli elementi che riguardano u
        for i in range(len(nb)): # prende uno per uno tutti i valori di nb
            u_element = np.array(u[i]) #seleziono l'i-esimo ingresso

            ex_order = nb[i]
            if ex_order != 0: #controllo che ex_order non sia 0: se così fosse, vorrebbe dire che non ho alcuna dipendenza da u e non scendo neanche nel ciclo.
                ex_delay = nk[i]
            
                for ex_trasl in range(ex_delay,ex_delay+ex_order):
                    u_trasl = u_element[(max_trasl-ex_trasl):(len(u_element)-(ex_trasl-min_trasl))] #effettuo la traslazione di u, ottenendo u(t-nk-1), u(t-nk-2)...
                    #print(len([u_trasl])) restuisce 1
                    #print(M.shape) restituisce (5, 1820, 1)
                    print("ok2")
                    print(np.shape(u_trasl))
                    M = np.append(M, [u_trasl], axis=0)
                    
        M=np.squeeze(M)
        M = np.transpose(M) #così ha tante righe quanti sono i dati usati e tante colonne quanti sono i valori di na + tt gli elem. di nb
        np.shape(M)
        # Ora rimane solo da fare un controllo sulla matrice M creata: potrebbe essere che la matrice abbia più righe di quelle che avrà y(t) una volta 
        # persi i valori a seguito delle traslazioni. Se così fosse, tolgo le ultime righe della M finchè non è lunga come y(t).
        #print(M.shape) 
        len_y_trasl = len(y)-max_trasl
        if len_y_trasl < M.shape[0]: #se y privata dei valori di traslazione è più corta del nr. di righe di M, allora M va accorciata
            M = M[0:(len_y_trasl),:]
            y_out = y[(max_trasl):(max_trasl+M.shape[0])]
        else:
            y_out = y[(max_trasl):(max_trasl+M.shape[0])]
       
        
        y_out = np.array(y_out) 

            
        M_tr = np.transpose(M)

        print(M_tr.shape)
        print(M.shape)
        teta = np.matmul(np.matmul(np.linalg.inv(np.matmul(M_tr,M)),M_tr),y_out)
        

        return(M,teta,y_out)
    
    else: #nel caso in cui l'orizzone di regressione sia più lungo dei dati
        raise Exception("Your dataset is not long enough to support the regression you asked!")
    




'''

def arx_sklearn(na,nb,nk,y,u,flag_positive, intercept_flag): 

    # riceve in ingresso il termine na e i due vettori nb e nk (vanno passati come vettori anche se hanno 1 elemento solo). 
    # riceve inoltre due vettori y e u, che sono i dati che abbiamo relativi rispettivamente all'input e all'output.
    # resituisce due elementi numpy: la matrice M e il vettore uscite y_out
    # procediamo subito a convertire tutti i vettori in array di numpy
    y = np.array(y)
    u = np.array(u)
    if len(u.shape)==1: #controllo su u, in modo che venga trattato come matrice anche nel caso in cui sia un semplice vettore
        u = np.array([u])
 
    nb = np.array(nb)
    nk = np.array(nk)
   
    #il vettore nbk conterrà le traslazioni date da nb e nk
    nbk = []

    for i in range(nb.size):
        for j in range(nk[i],nb[i]+nk[i]):
            nbk.append(j)
    


    #definiamo alcuni termini utili alla traslazione:
    na_nbk = np.concatenate(([na],nbk))
    
    max_trasl = max(na_nbk) # indica la massima traslazione che un vettore potrà subire.
    min_trasl = min(np.concatenate(([1],nbk))) # indica la minima traslazione che un vettore potrà subire. Se nel vettore nbk comparisse uno zero, min_trasl = 0, altrimenti
    # 1 perchè sicuramente una traslazione per y(t-1) ce l'abbiamo;


    len_M = y.size+min_trasl-max_trasl #e usiamo questo valore per controllare di avere abbastanza valori per la regressione richiesta:
    # infatti abbiamo problemi se questa len_M diventa 0, perchè vuole dire che la matrice M è vuota!

    if len_M>0:
               
        # ora riempiamo la matrice M con tutta la parte che riguarda y. Alla fine di questa parte, M avrà un numero di elementi pari al valore di na.
        for ar_order in range(1,na+1): # ovvero, per tutti i valori da 1 fino a na inclusi
            y_trasl = y[(max_trasl-ar_order):(len(y)-(ar_order-min_trasl))] #effettuo la traslazione di y, ottenendo y(t-1), y(t-2)...
            if ar_order == 1:
                M = np.array([y_trasl]) #inizializzazione matrice M
            else:
                M = np.append(M, [y_trasl], axis=0)
            

         # ora invece aggiungiamo alla matrice tutti gli elementi che riguardano u
        for i in range(len(nb)): # prende uno per uno tutti i valori di nb
            u_element = np.array(u[i]) #seleziono l'i-esimo ingresso
            ex_order = nb[i]
            if ex_order != 0: #controllo che ex_order non sia 0: se così fosse, vorrebbe dire che non ho alcuna dipendenza da u e non scendo neanche nel ciclo.
                ex_delay = nk[i]
            
                for ex_trasl in range(ex_delay,ex_delay+ex_order):
                    u_trasl = u_element[(max_trasl-ex_trasl):(len(u_element)-(ex_trasl-min_trasl))] #effettuo la traslazione di u, ottenendo u(t-nk-1), u(t-nk-2)...
                    M = np.append(M, [u_trasl], axis=0)
                    
        
        M = np.transpose(M) #così ha tante righe quanti sono i dati usati e tante colonne quanti sono i valori di na + tt gli elem. di nb
        
        # Ora rimane solo da fare un controllo sulla matrice M creata: potrebbe essere che la matrice abbia più righe di quelle che avrà y(t) una volta 
        # persi i valori a seguito delle traslazioni. Se così fosse, tolgo le ultime righe della M finchè non è lunga come y(t).
        #print(M.shape) 
        len_y_trasl = len(y)-max_trasl
        if len_y_trasl < M.shape[0]: #se y privata dei valori di traslazione è più corta del nr. di righe di M, allora M va accorciata
            M = M[0:(len_y_trasl),:]
            y_out = y[(max_trasl):(max_trasl+M.shape[0])]
        else:
            y_out = y[(max_trasl):(max_trasl+M.shape[0])]
       
        
        y_out = np.array(y_out) 


        #ora che ho trovato la M e la y, al posto che fare il calcolo del teta con le operazioni solite, lo faccio con sklearn
        #in modo da poter sfruttare la possibilità di avere coefficienti positivi

        #https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
          
        if flag_positive:
            if intercept_flag:
                teta = linear_model.LinearRegression(positive=True, fit_intercept=True)
                teta.fit(M, y_out)  
                model_skversion = teta
                intercept = teta.intercept_
                teta = np.array(teta.coef_)

            else:
                teta = linear_model.LinearRegression(positive=True,fit_intercept=False)
                teta.fit(M, y_out)  
                model_skversion = teta
                intercept = teta.intercept_
                teta = np.array(teta.coef_)
            
        else:
            if intercept_flag:
                teta = linear_model.LinearRegression(fit_intercept=True)
                teta.fit(M, y_out) 
                model_skversion = teta
                intercept = teta.intercept_ 
                teta = np.array(teta.coef_)

            else:
                teta = linear_model.LinearRegression(fit_intercept=False)
                teta.fit(M, y_out)  
                model_skversion = teta
                intercept = teta.intercept_
                teta = np.array(teta.coef_)

        return(M,teta,intercept,model_skversion)
    
    else: #nel caso in cui l'orizzonte di regressione sia più lungo dei dati
        raise Exception("Your dataset is not long enough to support the regression you asked!")
    


'''