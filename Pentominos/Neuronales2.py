# -*- coding: utf-8 -*-
import csv
import os 
import random 
import numpy as np
# from Pentominos.Modelo import *
# from Pentominos.Formas import modelo
from Pentominos.Utilidades import cargar_pentominos, rango_por_letra, posicion_real

# import pandas
import array
import sys

import pandas
import neurolab as nl
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


Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
Pentominos = []
NUM_ENT=1000    


def get_max(siguiente_letra, solucion):
    rangos = rango_por_letra(Formas)
#     pentominos = cargar_pentominos(Formas)
#     letras=np.array(Formas)
#     if np.count_nonzero(prueba)==0:
#         print("Tablero esta vacio")
#         state=[0,0]
#         letra=''
#         siguiente_letra='F'
#     else:
#         state = max([(prueba[i],i) for i in range(63)])
#         letra=pentominos[state[1]][0]
#         siguiente_letra=Formas[np.where(letras==letra)[0][0]+1]
#         print("Tablero no esta vacio, el estado es: "+str(state))
# 
#     print("Letra "+letra)
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
        
        
#     print("Letra: "+str(letra))
#     print("Siguiente_letra: "+str(siguiente_letra))
#     print("Mejor movimiento: "+str(action))
    
    return action
            
            
def crear_conjunto_entrenamiento(): #Darle solo los valores maximos, las que son mas prometedoras
    rangos = rango_por_letra(Formas)
#     pentominos = cargar_pentominos(Formas)
    if os.path.isfile('../Pentominos/csv/entrenamiento-v5.csv')==False:
        print("Fichero de entrenamiento no encontrado, procedemos a su creación")
        with open('../Pentominos/csv/entrenamiento-v5.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if os.path.isfile('../Pentominos/learning/alfabetico.txt')==True:
                print("Fichero qlearning encontrado")
                qtable=[[{} for i in range(64)] for _ in range(64)]
                with open("../Pentominos/learning/alfabetico.txt") as file:
                    i=0
                    for line in file: 
                        split1=line.split("}]")
                        split=split1[0].split("}, ")
                        j=0
                        for trozo in split:
                            trozo=trozo.strip('[{')
                            trozo=trozo.strip('\n')
                            if trozo!='':
                                posibles=trozo.split(', ')
                                for p in posibles:
                                    real=p.split(': ')
                                    dic={real[0].strip("'"):float(real[1])}
                                    qtable[i][j].update(dic)
                            j+=1
                        i+=1
                
                
            letra_i=0
            keys=[]
            for i in range(len(qtable)):
                row=qtable[i]
                letra=Formas[letra_i]
                zona=rangos[letra]
                print("Letra "+str(letra))
#                 print("Row "+str(row))
                
#                 row_plano = np.squeeze(np.asarray(row))
                row_cortado_diccionario=row[zona[0]:zona[1]+1]
                print("Row Cortado Diccionario "+str(row_cortado_diccionario))
                for dictio in row_cortado_diccionario:
                    for key in dictio.keys():
                        if key not in keys:
                            keys.append(key)
                            row_cortado=[]
                            for dic in row_cortado_diccionario:
                                if key in dic:
                                    row_cortado.append(dic[key])
                                else:
                                    row_cortado.append(0.0)
                            row_cortado=np.copy(row_cortado)
                        
                            row_maximo = np.where(row_cortado==np.amax(row_cortado)) #cogemos los indices que tengan el valor maximo
                            rand = random.randint(0,len(row_maximo[0])-1)
                            row_relativo = row_maximo[0][rand] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
                            action=posicion_real(row_relativo, letra, Formas) #obtenemos el indice real ya que le anterior era el indice ralivo al array cortado
                 
    #                         action+=1 #Sumamos uno para contar en la tabla el hueco para la posicion 0
                            entrada=[]
                            counter=0
                            inicio=2
                            for numero in key:
                                if inicio>0:
                                    entrada.append(int(numero))
                                    inicio-=1
                                elif counter==0:
                                    counter+=int(numero)*10
                                else:
                                    counter+=int(numero)
                                    entrada.append(counter)
                                    counter=0
                            filewriter.writerow([np.copy(entrada), action])
                            if action==11 or action==12 or action==17 or action==2 or action==8:
                                filewriter.writerow([np.copy(entrada), action])
                    
                
                if i==zona[0]-1 or letra=='F':
                    letra_i+=1
                    
                if letra=='Z':
                    break
                    
        print ("Completada la creacion de entrenamiento-v5.csv")
    else:
        print("Fichero encontrado")
    
            
def get_entrada_objetivo():
    crear_conjunto_entrenamiento()
    partidas=pandas.read_csv('../Pentominos/csv/entrenamiento-v5.csv', header=None, names=['State', 'Action'])
#     with open('csv/entrenamiento-v4.csv', 'r', encoding="utf8") as f:
#         reader = csv.reader(f)
#         for row in reader:
#             if row!=[]: #Genera filas vacias, NO SE PORQUE
#                 partidas.append([int(row[0]),int(row[1])])
#     print("Partidas: ")
#     print(partidas)
    conjunto_entrenamiento, conjunto_prueba = train_test_split(partidas, test_size=.33, random_state=2346523, stratify=partidas['Action'])
    
#    CROSS VAL SCORE
#     estimator = linear_model.Lasso()
#     scores=cross_val_score(estimator, partidas,partidas['Action'], cv=10)
#       
#     print("Resultados cros_val_score: "+str(scores))
    
    entrada_str=conjunto_entrenamiento['State']
    prueba_str=conjunto_prueba['State']
#     print("Entrenamiento: ")
#     print(entrada_str)
#     print("Prueba: ")
#     print(prueba_str)
    
    objetivo=[] 
    for ficha in conjunto_entrenamiento['Action']:
        aux=[0]*63
        aux[ficha]=1
        objetivo.append(aux)
    entrada=[]
    for row in entrada_str:
        aux=[0]*10
        primeros=2
        acumulador=0
        n=0
        for i in row:
            if i.isdigit():
                if primeros>0:
                    aux[n]+=int(i)
                    primeros-=1
                    n+=1
                elif acumulador==0:
                    acumulador+=int(i)*10
                else:
                    acumulador+=int(i)
                    aux[n]+=acumulador
                    acumulador=0
                    n+=1
        entrada.append(aux)
    prueba=[]
    for row in prueba_str:
        aux=[0]*10
        primeros=2
        acumulador=0
        n=0
        for i in row:
            if i.isdigit():
                if primeros>0:
                    aux[n]+=int(i)
                    primeros-=1
                    n+=1
                elif acumulador==0:
                    acumulador+=int(i)*10
                else:
                    acumulador+=int(i)
                    aux[n]+=acumulador
                    acumulador=0
                    n+=1
        prueba.append(aux)
        
    return np.array(entrada), np.array(objetivo), np.array(prueba)
            

def red_neuronal(): #Parametros de entrada para el tamaño del tablero
    if os.path.isfile('../Pentominos/redes/nueva-red.net')==False:
        funcion_activacion = trans.LogSig() #TODO probar otras funciones de activacion
    #     valores_entrada=[[i] for i in range(1,63)]
    #     valores_entrada.append([1,63])
        red = net.newff(minmax=[[0,63]]*10, size=[4,4,63], transf=[funcion_activacion]*3)
        red.reset()
        entrada, objetivo, prueba = get_entrada_objetivo()
    
        #Sesgos y pesos iniciales
        np.random.seed(3287426346)    
    #     red.reset()
        for capa in red.layers:
            capa.initf=init.InitRand([0,63], 'bw') #Se puede poner a 0
         
        red.init()   
        
        red.trainf = train.train_gd #TODO probar otros tipos de entrenamiento
        red.errorf = error.MAE() #TODO probar otros tipos de errores
        
    #     print red.layers[0].np
    #     print red.layers[1].np
        
        print ("Comienza el entrenamiento")
        print("Net.ci: "+str(red.ci))
         
        red.train(entrada, objetivo, lr=0.1, epochs=1000, show=10, goal=0.01)
         
    #     print red.layers[0].np
    #     print red.layers[1].np
        red.sim(prueba)
        red.save('../Pentominos/redes/nueva-red.net')
    #     return red.sim(prueba), prueba
    else:
        red = nl.load('../Pentominos/redes/nueva-red.net')
    return red


if __name__=="__main__":
#     tablero = Tablero(8,8)
#     entrada, objetivo, prueba=get_entrada_objetivo()
#     print("Entrada")
#     print(entrada)
#     print(test_a)
#     print("Shape: "+str(entrada.shape[1]))
#     print("Objetivo")
#     print(objetivo)
#     print("Prueba")
#     print(prueba)
    
    red_neuronal()
#     for s in range(len(solucion)):
#         print(" ")
#         print("Estado, Accion: "+str(get_max(prueba[s],solucion[s])))
    
#     inicio(8,8,2)
#     introduciendo_letras(1000)
#     print colocar_fichas_random(tablero)
#     crear_conjunto_entrenamiento(1000)
#     busqueda_profunidad()
    
# #     conjunto_correcto()
#     salida, tableros = red_neuronal()
#     print salida
#     for i in range(len(tableros)):
#         print tableros[i]
#         print get_max(salida[i])
        
#     for pieza in salida:
#         print get_max(pieza)

#Estratificado y probar si la red aprende
#Visualización
#Conjunto de entrenamiento realista

    
        
        
    