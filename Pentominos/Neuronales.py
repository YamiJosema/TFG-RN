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

# def crear_pentominos_csv():
#     no_inversa=["T","U","V","W"]
#     with open('csv/pentominos.csv', 'wb') as csvfile:
#         filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         for i in Formas:
#             if i=="X":
#                 filewriter.writerow(["X",0,0])
#             elif i=="I":
#                 filewriter.writerow(["I",0, 0])
#                 filewriter.writerow(["I",1, 0])
#             elif i=="Z":
#                 filewriter.writerow(["Z",0, 0])
#                 filewriter.writerow(["Z",1, 0])
#                 filewriter.writerow(["Z",0, 1])
#                 filewriter.writerow(["Z",1, 1])
#             else:
#                 for j in range(4):
#                     filewriter.writerow([i,j,0])
#                     if i not in no_inversa:
#                         filewriter.writerow([i,j,1])
#         

# def cargar_pentominos():
#     if os.path.isfile('csv/pentominos.csv')==False:
#         crear_pentominos_csv()
#     
#     with open('csv/pentominos.csv', 'rb') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             Pentominos.append(row)


# def colocar_fichas_random(tablero):
#     fichas_colocadas = []
#     letras=[]
#     no_inversa=["T","U","V","W"]
#     letras.extend(tablero.pentominos)
#     cargar_pentominos()
# #     tablero = Tablero(x,y)
#     i=0
#     j=0
# #     while tablero.todos_usados():
#     colocado = False
#     contador=0
#     for i in range(tablero.x):
#         for j in range(tablero.y):
# #             print "("+str(i)+", "+str(j)+")"
#             if tablero.board[i][j]==0:
# #                 print tablero
#                 while (not colocado) and contador<len(letras):
#                     letra = letras[random.randint(0, len(letras)-1)]
#                     for rotacion in range(4):  #solucionar que empiece siempre por 00 TODO
#                         for invertido in range(2):
#                             if letra in no_inversa:
#                                 invertido=0
#                             pentomino = Pentomino(letra,rotacion,invertido)
#                             colocado = tablero.colocar_sin_superposicion(pentomino, i, j)
#                             if colocado==True:
#                                 ficha=[letra, rotacion, invertido]
#                                 ficha = Pentominos.index([letra,str(rotacion),str(invertido)])
#                                 fichas_colocadas.append(ficha)
#                                 break
#                         if colocado==True:
#                             break
#                     contador+=1
# #                 print "-------------------------------------"
# #                 print "Letra: "+letra+" de "+str(letras)
# #                 print "Contador: "+str(contador)
#                 if colocado==True:
#                     letras.remove(letra)
#                 colocado=False
#                 contador=0
# #     return letras, tablero
#     return fichas_colocadas


# def introduciendo_letras(n):
#     letra = raw_input("Selecciona pentomino de entre [F, I, L, N, P, T, U, V, W, X, Y, Z]\n") #Solo input en python 3
#     while letra not in Formas:
#         letra = raw_input("Incorrecto. Selecciona pentomino de entre [F, I, L, N, P, T, U, V, W, X, Y, Z]\n") #Solo input en python 3
#     
#     victoria = []
#     save = []
#     for i in range(n):
#         tablero = Tablero(8,8)
#         pentomino = Pentomino(letra)
#         tablero.colocar_sin_superposicion(pentomino, 0, 0)
#         result=colocar_fichas_random(tablero)
#         if len(result[0])<len(save) or not save:
#             save=result[0]
#             victoria=result[1]
#     print save
#     print victoria
        
        
# def conjunto_correcto():
#     crear_conjunto_entrenamiento(8,8)
#     partidas = pandas.read_csv('csv/entrenamiento.csv', header=None, names=['Tablero', 'Ficha'])
#     contador=[0]*63
#     for p in partidas['Ficha']:
#         contador[p]+=1
#     borrar=[]
#     for i in range(len(contador)):
#         if contador[i]==1:
#             borrar.append(i)
#     
#     with open('csv/entrenamiento-v1.csv', 'wb') as csvfile:
#         filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         with open('csv/entrenamiento.csv', 'rb') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 if int(row[1]) not in borrar:
#                     filewriter.writerow([row[0], row[1]])
                    
                    
def get_pentominos():
    return Pentominos


def get_max(prueba, solucion):
    rangos = rango_por_letra(Formas)
    pentominos = cargar_pentominos(Formas)
    letras=np.array(Formas)
    if np.count_nonzero(prueba)==0:
        print("Tablero esta vacio")
        state=[0,0]
        letra=''
        siguiente_letra='F'
    else:
        state = max([(prueba[i],i) for i in range(63)])
        letra=pentominos[state[1]][0]
        siguiente_letra=Formas[np.where(letras==letra)[0][0]+1]
        print("Tablero no esta vacio, el estado es: "+str(state))

    print("Letra "+letra)
    print("Siguiente letra "+str(siguiente_letra))
    
    zona=rangos[siguiente_letra]
    print("Zona "+str(zona))
    solucion_cortado=solucion[zona[0]:zona[1]+1]
    print("Cortado "+str(solucion_cortado))
    solucion_maximo = np.where(solucion_cortado==np.amax(solucion_cortado)) #cogemos los indices que tengan el valor maximo
    solucion_relativo = solucion_maximo[0][0]
    action=posicion_real(solucion_relativo, siguiente_letra, Formas)
    print("Action "+str(action))
        
        
#     print("Letra: "+str(letra))
#     print("Siguiente_letra: "+str(siguiente_letra))
#     print("Mejor movimiento: "+str(action))
    
    return state[1], action
            
            
def crear_conjunto_entrenamiento(): #Darle solo los valores maximos, las que son mas prometedoras
    rangos = rango_por_letra(Formas)
    pentominos = cargar_pentominos(Formas)
    if os.path.isfile('../Pentominos/csv/entrenamiento-v4.csv')==False:
        print("Fichero de entrenamiento no encontrado, procedemos a su creación")
        with open('../Pentominos/csv/entrenamiento-v4.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if os.path.isfile('../Pentominos/learning/alfabetico.txt')==True:
                print("Fichero qlearning encontrado")
                qtable = np.loadtxt('../Pentominos/learning/alfabetico.txt', dtype=float32)
                
            letra_i=0
            for row in range(len(qtable)):
                print("Fila "+str(row))
                letra=Formas[letra_i]
                zona=rangos[letra]
                
                row_plano = np.squeeze(np.asarray(qtable[row]))
                row_cortado=row_plano[zona[0]:zona[1]+1]
                row_maximo = np.where(row_cortado>0.0)
                
                if len(row_maximo[0])==0:
                    row_maximo = np.where(row_cortado==np.amax(row_cortado))
                
                print("Letra "+letra)
                print('Zonas:'+str(zona))
                print('Fila cortada:'+str(row_cortado))
                print("Maximos: "+str(row_maximo[0]))
                
                for index in row_maximo[0]:
                    if row_cortado[index]!=0:
                        action=posicion_real(index, letra[0], Formas)+1
                        print("State:"+str(row)+", Action:"+str(action))
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
        aux[ficha-1]=1
        objetivo.append(aux)
    entrada=[] #TODO convertir en array con 1 en la entrada (como objetivo)
    for row in entrada_str:
        aux=[0]*63
        aux[int(row)]=1
#         ent=row.replace("[", "")
#         ent2=ent.replace("]", "")
#         entrada.append(map(int,[row]))
        entrada.append(aux)
    prueba=[]
    for row in prueba_str:
        aux=[0]*63
        aux[int(row)]=1
#         prb=row.replace("[", "")
#         prb2=prb.replace("]", "")
#         prueba.append(map(int,[row]))
        prueba.append(aux)
        
    return np.array(entrada), np.array(objetivo), np.array(prueba)
            

def red_neuronal(): #Parametros de entrada para el tamaño del tablero
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
     
    red.train(entrada, objetivo, lr=0.1, epochs=10000, show=500, goal=0.01)
     
#     print red.layers[0].np
#     print red.layers[1].np
    red.sim(prueba)
#     return red.sim(prueba), prueba
    return red


if __name__=="__main__":
#     tablero = Tablero(8,8)
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

    
        
        
    