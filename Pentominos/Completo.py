# -*- coding: utf-8 -*-
import csv
import os 
import random 
import numpy as np

# import pandas
import array
import sys

import pandas
from neurolab import init
from neurolab import trans
from neurolab import train
from neurolab import error
from neurolab import net
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import linear_model
from numpy import float32
# from theano.tensor.basic import row
# from numpy.f2py.rules import aux_rules


Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"] #ORDEN

#------------------------Utilidades--------------------------------------
def cargar_pentominos(orden):
    pentominos=[]
    if os.path.isfile('csv/pentominos.csv')==False: #TODO
        crear_pentominos_csv(orden)
    
    with open('csv/pentominos.csv', 'r', encoding="utf8") as f: #TODO
        reader = csv.reader(f)
        for row in reader:
            if row!=[]: #Genera filas vacias a veces
                pentominos.append(row)
    return pentominos


def crear_pentominos_csv(orden):
    no_inversa=["T","U","V","W"]
    with open('csv/pentominos.csv', 'w') as csvfile: #TODO
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in orden:
            if i=="X":
                filewriter.writerow(["X",0,0])
            elif i=="I":
                filewriter.writerow(["I",0, 0])
                filewriter.writerow(["I",1, 0])
            elif i=="Z":
                filewriter.writerow(["Z",0, 0])
                filewriter.writerow(["Z",1, 0])
                filewriter.writerow(["Z",0, 1])
                filewriter.writerow(["Z",1, 1])
            else:
                for j in range(4):
                    filewriter.writerow([i,j,0])
                    if i not in no_inversa:
                        filewriter.writerow([i,j,1])
                        

def rango_por_letra(orden):
    rangos={}
    posicion=1
    cuatro_posiciones=["T","U","V","W","Z"]
    for letra in orden:
        if letra in cuatro_posiciones:
            rangos[letra]=(posicion,posicion+3)
            posicion+=4
        elif letra=="X":
            rangos[letra]=(posicion,posicion)
            posicion+=1
        elif letra=="I":
            rangos[letra]=(posicion,posicion+1)
            posicion+=2
        else:
            rangos[letra]=(posicion,posicion+7)
            posicion+=8
    return rangos      


def posicion_real(posicion, letra, orden):
    posicion_real=posicion
    cuatro_posiciones=["T","U","V","W","Z"]
    for l in orden:
        if l!=letra:
            if l in cuatro_posiciones:
                posicion_real+=4
            elif l=="X":
                posicion_real+=1
            elif l=="I":
                posicion_real+=2
            else:
                posicion_real+=8
        if l==letra:
            break
    return posicion_real
#------------------------------------------------------------------------

#-------------------Neuronales--------------------------------------
def get_max(prueba, solucion):
    rangos = rango_por_letra(Formas)
    pentominos = cargar_pentominos(Formas)
    state = max([(prueba[i],i) for i in range(63)])
    action=-1
    siguiente_letra=-1
    letra=pentominos[state[1]][0]
    if letra!='Z':
        letras=np.array(Formas)
        
        siguiente_letra=Formas[np.where(letras==letra)[0][0]+1]
        
        zona=rangos[siguiente_letra]
        solucion_cortado=solucion[zona[0]:zona[1]+1]
        solucion_maximo = np.where(solucion_cortado==np.amax(solucion_cortado)) #cogemos los indices que tengan el valor maximo
        solucion_relativo = solucion_maximo[0][0]
        action=posicion_real(solucion_relativo, siguiente_letra, Formas)
#     print("Letra: "+str(letra))
#     print("Siguiente_letra: "+str(siguiente_letra))
#     print("Mejor movimiento: "+str(action))
    
    return state[1], action
            
            
def crear_conjunto_entrenamiento(): #Darle solo los valores maximos, las que son mas prometedoras
    rangos = rango_por_letra(Formas)
    pentominos = cargar_pentominos(Formas)
    if os.path.isfile('csv/entrenamiento-v4.csv')==False:
        with open('csv/entrenamiento-v4.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if os.path.isfile('../Pentominos/learning/alfabetico.txt')==True:
                print("Fichero qlearning encontrado")
                qtable = np.loadtxt('../Pentominos/learning/alfabetico.txt', dtype=float32)
            for row in range(len(qtable)):
                letra=pentominos[row]
                row_plano = np.squeeze(np.asarray(qtable[row]))
                zona=rangos[letra] 
                row_cortado=row_plano[zona[0]:zona[1]+1]
                row_maximo = np.where(row_cortado==np.amax(row_cortado))
        #             print("Fila: "+str(row_plano))
                for i in range(len(row_maximo[0])):
                    if row_maximo[0][i] != 0:
                        action=posicion_real(row_maximo[0][i], letra, Formas)
                        filewriter.writerow([row, action])
                        filewriter.writerow([row, action])
                    
        print ("Completada la creacion de entrenamiento-v4.csv")
    else:
        print("Fichero encontrado")
    
            
def get_entrada_objetivo():
    partidas=pandas.read_csv('csv/entrenamiento-v4.csv', header=None, names=['State', 'Action']) #TODO
    conjunto_entrenamiento, conjunto_prueba = train_test_split(partidas, test_size=.33, random_state=2346523, stratify=partidas['Action'])
    
#--------------------------CROSS VAL SCORE---------------------------
#     estimator = linear_model.Lasso()
#     scores=cross_val_score(estimator, partidas,partidas['Action'], cv=10)
#       
#     print("Resultados cros_val_score: "+str(scores))
#------------------------------------------------------------------    
    
    entrada_str=conjunto_entrenamiento['State']
    prueba_str=conjunto_prueba['State']
#     print("Entrenamiento: ")
#     print(entrada_str)
#     print("Prueba: ")
#     print(prueba_str)
    
    objetivo=[] 
    for ficha in conjunto_entrenamiento['Action']:
        aux=[0]*63
        aux[ficha-1]=1
        objetivo.append(aux)
    entrada=[] #TODO convertir en array con 1 en la entrada (como objetivo)
    for row in entrada_str:
        aux=[0]*63
        aux[int(row)]=1
        entrada.append(aux)
    prueba=[]
    for row in prueba_str:
        aux=[0]*63
        aux[int(row)]=1
        prueba.append(aux)
        
    return np.array(entrada), np.array(objetivo), np.array(prueba)
            

def red_neuronal():
    funcion_activacion = trans.LogSig() #TODO probar otras funciones de activacion
#     valores_entrada=[[i] for i in range(1,63)]
#     valores_entrada.append([1,63])
    red = net.newff(minmax=[[0,1]]*63, size=[5,5,63], transf=[funcion_activacion]*3)
    red.reset()
    entrada, objetivo, prueba = get_entrada_objetivo()

    #Sesgos y pesos iniciales
    np.random.seed(3287426346)    
#     red.reset()
    for capa in red.layers:
        capa.initf=init.init_zeros #InitRand([-1,1], 'bw') #Se puede poner a 0
     
    red.init()   
    
    red.trainf = train.train_gd
    red.errorf = error.MAE() #TODO probar otros tipos de errores
    
#     print red.layers[0].np
#     print red.layers[1].np
    
    print ("Comienza el entrenamiento")
    print("Net.ci: "+str(red.ci))
     
    red.train(entrada, objetivo, lr=0.1, epochs=2000, show=100, goal=0.01)
     
#     print red.layers[0].np
#     print red.layers[1].np
    return red.sim(prueba), prueba
#     return red


if __name__=="__main__":
#     tablero = Tablero(8,8)
    crear_conjunto_entrenamiento()
    entrada, objetivo, prueba=get_entrada_objetivo()
#     print("Entrada")
#     print(entrada)
#     print(test_a)
#     print("Shape: "+str(entrada.shape[1]))
#     print("Objetivo")
#     print(objetivo)
#     print("Prueba")
#     print(prueba)
    
    solucion, prueba=red_neuronal()
    for s in range(len(solucion)):
        print(" ")
        print("Estado, Accion: "+str(get_max(prueba[s],solucion[s])))
    
    print("FINAL")
        


