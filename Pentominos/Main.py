# -*- coding: utf-8 -*-
import csv
import os 
import random 
import numpy as np
from Modelo import *
from Formas import modelo

import pandas
import array

from neurolab import init
from neurolab import trans
from neurolab import train
from neurolab import error
from neurolab import net
from sklearn import cross_validation
# from theano.tensor.basic import row
# from numpy.f2py.rules import aux_rules


Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
Pentominos = []
NUM_ENT=1000    

def crear_pentominos_csv():
    no_inversa=["T","U","V","W"]
    with open('csv/pentominos.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in Formas:
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
        

def cargar_pentominos():
    if os.path.isfile('csv/pentominos.csv')==False:
        crear_pentominos_csv()
    
    with open('csv/pentominos.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            Pentominos.append(row)


def colocar_fichas_random(tablero):
    fichas_colocadas = []
    letras=[]
    no_inversa=["T","U","V","W"]
    letras.extend(tablero.pentominos)
    cargar_pentominos()
#     tablero = Tablero(x,y)
    i=0
    j=0
#     while tablero.todos_usados():
    colocado = False
    contador=0
    for i in range(tablero.x):
        for j in range(tablero.y):
#             print "("+str(i)+", "+str(j)+")"
            if tablero.board[i][j]==0:
#                 print tablero
                while (not colocado) and contador<len(letras):
                    letra = letras[random.randint(0, len(letras)-1)]
                    for rotacion in range(4):  #solucionar que empiece siempre por 00 TODO
                        for invertido in range(2):
                            if letra in no_inversa:
                                invertido=0
                            pentomino = Pentomino(letra,rotacion,invertido)
                            colocado = tablero.colocar_sin_superposicion(pentomino, i, j)
                            if colocado==True:
                                ficha=[letra, rotacion, invertido]
                                ficha = Pentominos.index([letra,str(rotacion),str(invertido)])
                                fichas_colocadas.append(ficha)
                                break
                        if colocado==True:
                            break
                    contador+=1
#                 print "-------------------------------------"
#                 print "Letra: "+letra+" de "+str(letras)
#                 print "Contador: "+str(contador)
                if colocado==True:
                    letras.remove(letra)
                colocado=False
                contador=0
#     return letras, tablero
    return fichas_colocadas


def introduciendo_letras(n):
    letra = raw_input("Selecciona pentomino de entre [F, I, L, N, P, T, U, V, W, X, Y, Z]\n") #Solo input en python 3
    while letra not in Formas:
        letra = raw_input("Incorrecto. Selecciona pentomino de entre [F, I, L, N, P, T, U, V, W, X, Y, Z]\n") #Solo input en python 3
    
    victoria = []
    save = []
    for i in range(n):
        tablero = Tablero(8,8)
        pentomino = Pentomino(letra)
        tablero.colocar_sin_superposicion(pentomino, 0, 0)
        result=colocar_fichas_random(tablero)
        if len(result[0])<len(save) or not save:
            save=result[0]
            victoria=result[1]
    print (save)
    print (victoria)
        
        
def crear_conjunto_entrenamiento(x,y):
    with open('csv/entrenamiento.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        num_fichas=int((x*y)/5)
        ent_count=int(NUM_ENT/num_fichas-1)
        loop=0
        cut = 0
        for _ in range(NUM_ENT):
            tablero = Tablero(x,y)
            fichas = colocar_fichas_random(tablero)
#             num=len(fichas)
#             cut = 0 #random.randint(0, num-2)
            if cut>=len(fichas):
                cut=len(fichas)-1
            entrada=np.array(fichas[:cut])
            entrada_cero = np.zeros(num_fichas-len(entrada),dtype=np.int)
            if len(entrada_cero)!=num_fichas:
                entrada_cero=np.concatenate((entrada, entrada_cero), axis=None)
            objetivo=fichas[cut];
            filewriter.writerow([entrada_cero, objetivo])
            loop+=1
            if loop==ent_count:
                loop=0
                cut+=1
        
    print ("Completada la creacion de entrenamiento.csv")


def get_max(array):
    m = max([(array[i],i) for i in range(63)])
    return m[1]
            
            
def get_entrada_objetivo(x,y):
    partidas = pandas.read_csv('csv/entrenamiento-v1.csv', header=None, names=['Tablero', 'Ficha'])
    conjunto_entrenamiento, conjunto_prueba = cross_validation.train_test_split(partidas, test_size=.33, random_state=2346523, stratify=partidas['Ficha'])
    entrada_str=conjunto_entrenamiento['Tablero']
    prueba_str=conjunto_prueba['Tablero']
    
    objetivo=[]
    for ficha in conjunto_entrenamiento['Ficha']:
        aux=[0]*63
        aux[ficha]=1
        objetivo.append(aux)
    entrada=[]
    for row in entrada_str:
        ent=row.replace("[", "")
        ent2=ent.replace("]", "")
        entrada.append(map(int,ent2.split()))
    prueba=[]
    for row in prueba_str:
        prb=row.replace("[", "")
        prb2=prb.replace("]", "")
        prueba.append(map(int,prb2.split()))
    
    return entrada, objetivo, prueba
            

def red_neuronal(): #Parametros de entrada para el tamaño del tablero
    funcion_activacion = trans.LogSig()
#     valores_entrada=[[i] for i in range(1,63)]
#     valores_entrada.append([1,63])
    red = net.newff(minmax=[[1,63],[1,63],[1,63],[1,63],[1,63],[1,63],[1,63],[1,63],[1,63],[1,63],[1,63],[1,63]], size=[4,63], transf=[funcion_activacion]*2)
    red.reset()
    entrada, objetivo, prueba = get_entrada_objetivo(8, 8)

    #Sesgos y pesos iniciales
    np.random.seed(3287426346)    
#     red.reset()
    for capa in red.layers:
        capa.initf=init.init_zeros #InitRand([-1,1], 'bw') #Se puede poner a 0
     
    red.init()   
    
    red.trainf = train.train_gd
    red.errorf = error.SSE()
    
#     print red.layers[0].np
#     print red.layers[1].np
    
    print ("Comienza el entrenamiento")
     
    red.train(entrada, objetivo, lr=0.1, epochs=1000, show=100, goal=0.001)
     
#     print red.layers[0].np
#     print red.layers[1].np
    
    return red.sim(prueba), prueba
#     return red


def conjunto_correcto():
    crear_conjunto_entrenamiento(8,8)
    partidas = pandas.read_csv('csv/entrenamiento.csv', header=None, names=['Tablero', 'Ficha'])
    contador=[0]*63
    for p in partidas['Ficha']:
        contador[p]+=1
    borrar=[]
    for i in range(len(contador)):
        if contador[i]==1:
            borrar.append(i)
    
    with open('csv/entrenamiento-v1.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open('csv/entrenamiento.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if int(row[1]) not in borrar:
                    filewriter.writerow([row[0], row[1]])
                    
                    
def get_pentominos():
    return Pentominos
                    

if __name__=="__main__":
    tablero = Tablero(8,8)
#     inicio(8,8,2)
#     introduciendo_letras(1000)
#     print colocar_fichas_random(tablero)
#     crear_conjunto_entrenamiento(1000)
#     busqueda_profunidad()
    
    conjunto_correcto()
    salida, tableros = red_neuronal()
    print (salida)
    for i in range(len(tableros)):
        print (tableros[i])
        print (get_max(salida[i]))
        
#     for pieza in salida:
#         print get_max(pieza)

#Estratificado y probar si la red aprende
#Visualización
#Conjunto de entrenamiento realista

    
        
        
    
