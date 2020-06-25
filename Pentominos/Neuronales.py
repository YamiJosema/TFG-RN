# -*- coding: utf-8 -*-
'''
@author: Jose Manuel Pallero Hidalgo
@email: josemapallero29@gmail.com
'''

import csv
import os 
import numpy as np
# from Pentominos.Modelo import *
# from Pentominos.Formas import modelo
from Pentominos.Utilidades import rango_por_letra, posicion_real

# import pandas

import pandas
import neurolab as nl
from neurolab import init
from neurolab import trans
from neurolab import train
from neurolab import error
from neurolab import net
from sklearn.model_selection import train_test_split
from numpy import float32
# from theano.tensor.basic import row
# from numpy.f2py.rules import aux_rules


Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
Pentominos = []
NUM_ENT=1000    


def get_max(siguiente_letra, solucion):
    rangos = rango_por_letra(Formas)
    print("Siguiente letra "+str(siguiente_letra))
    
    zona=rangos[siguiente_letra]
    print("Zona "+str(zona))
    solucion_cortado=solucion[zona[0]:zona[1]+1]
    print("Cortado "+str(solucion_cortado))
    solucion_maximo = np.where(solucion_cortado==np.amax(solucion_cortado)) #cogemos los indices que tengan el valor maximo
    print("Maximo "+str(solucion_maximo))
    solucion_relativo = solucion_maximo[0][0]
    action=posicion_real(solucion_relativo, siguiente_letra, Formas)
    print("Action "+str(action))
        
        
    return action
            
            
def crear_conjunto_entrenamiento(): #Darle solo los valores maximos, las que son mas prometedoras
    rangos = rango_por_letra(Formas)
#     pentominos = cargar_pentominos(Formas)
    if os.path.isfile('../Pentominos/csv/entrenamiento-v4.csv')==False:
        print("Fichero de entrenamiento no encontrado, procedemos a su creación")
        with open('../Pentominos/csv/entrenamiento-v4.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if os.path.isfile('../Pentominos/learning/alfabetico.txt')==True:
                print("Fichero qlearning encontrado")
                qtable = np.loadtxt('../Pentominos/learning/alfabetico.txt', dtype=float32)
                
            letra_i=0
            for row in range(len(qtable)):
#                 print("Fila "+str(row))
                letra=Formas[letra_i]
                zona=rangos[letra]
                
                row_plano = np.squeeze(np.asarray(qtable[row]))
                row_cortado=row_plano[zona[0]:zona[1]+1]
                
                row_maximo = np.where(row_cortado==np.amax(row_cortado))
                
                for index in row_maximo[0]:
                    action=posicion_real(index, letra[0], Formas)
                    filewriter.writerow([row, action])
                    filewriter.writerow([row, action])
                
                if row==zona[0]-1 or letra=='F':
                    letra_i+=1
                    
                if letra=='Z':
                    break
                    
        print ("Completada la creacion de entrenamiento-v4.csv")
    else:
        print("Fichero encontrado")
    
            
def get_entrada_objetivo():
    crear_conjunto_entrenamiento()
    partidas=pandas.read_csv('../Pentominos/csv/entrenamiento-v4.csv', header=None, names=['State', 'Action'])
    conjunto_entrenamiento, conjunto_prueba = train_test_split(partidas, test_size=.33, random_state=2346523, stratify=partidas['Action'])
    
    
    entrada_str=conjunto_entrenamiento['State']
    prueba_str=conjunto_prueba['State']
    
    objetivo=[] 
    for ficha in conjunto_entrenamiento['Action']:
        aux=[0]*63
        aux[ficha]=1
        objetivo.append(aux)
    entrada=[]
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
            

def red_neuronal(): #Parametros de entrada para el tamaño del tablero
    if os.path.isfile('../Pentominos/redes/red-50k-onlymax.net')==False:
        funcion_activacion = trans.LogSig() 
        red = net.newff(minmax=[[0,1]]*63, size=[7,7,63], transf=[funcion_activacion]*3)
        red.reset()
        entrada, objetivo, prueba = get_entrada_objetivo()
    
        #Sesgos y pesos iniciales
        np.random.seed(3287426346)    
    #     red.reset()
        for capa in red.layers:
            capa.initf=init.init_zeros 
         
        red.init()   
        
        red.trainf = train.train_gd 
        red.errorf = error.MAE() 
        
        
        print ("Comienza el entrenamiento")
        print("Net.ci: "+str(red.ci))
         
        red.train(entrada, objetivo, lr=0.1, epochs=50000, show=500, goal=0.01)
         
        red.sim(prueba)
        red.save('../Pentominos/redes/red-50k-onlymax.net')
    #     return red.sim(prueba), prueba
    else:
        red = nl.load('../Pentominos/redes/red-50k-onlymax.net')
    return red

