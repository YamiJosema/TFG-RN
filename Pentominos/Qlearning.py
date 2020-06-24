# -*- coding: utf-8 -*-
'''
@author: Jose Manuel Pallero Hidalgo
'''
import numpy as np
import random
import os
from Pentominos.Utilidades import cargar_pentominos, rango_por_letra, posicion_real


def qlearning(tablero, modo=0, epochs=40000, gamma=0.4, epsilon=0.95, decay=0.001, limit=200):
    fichero='../Pentominos/learning/alfabetico.txt'
    if modo==2:
        fichero='../Pentominos/learning/esquinas.txt'
    elif modo==3:
        fichero='../Pentominos/learning/centro.txt'
    if os.path.isfile(fichero)==True:
        qtable=[[{} for i in range(64)] for _ in range(64)]
        with open(fichero) as file:
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
#                             print(real)
                            dic={real[0].strip("'"):float(real[1])}
                            qtable[i][j].update(dic)
                    j+=1
                i+=1
        
        print("Fichero qlearning encontrado")
#         qtable = np.loadtxt('../Pentominos/learning/alfabetico.txt', dtype=float32)
    else:
        print("Fichero no encontrado, pasamos a hacer el proceso de aprendizaje, esto llevara unos segundos")
        modo_aux=modo
        orden = tablero.pentominos
        pentominos = cargar_pentominos(orden)
        no_colocadas=[]
        rangos = rango_por_letra(orden)
        
        qtable=[[{} for i in range(len(pentominos)+1)] for _ in range(len(pentominos)+1)]
        
        for i in range(epochs):
            state, penalty, done = tablero.reset(orden,modo)
            steps = 0
            
            no_colocadas=[]
            fila_aux=[]
            last_state=state
            while not done:
                letra_actual=tablero.pentominos[0]
                if last_state!=state or not np.any(fila_aux):
                    fila_aux=np.copy(qtable[state])
                last_state=state
                
                key=get_key(tablero)
                action_completo = fila_aux
                action_plano = np.squeeze(np.asarray(action_completo))
                zona=rangos[tablero.pentominos[0]]
                action_cortado_diccionario=action_plano[zona[0]:zona[1]+1]
                action_cortado=[]
                for dic in action_cortado_diccionario:
                    if key in dic:
                        action_cortado.append(dic[key])
                    else:
                        action_cortado.append(0.0)
                action_cortado=np.copy(action_cortado)
                    
                if np.random.uniform() < epsilon:
                    if np.count_nonzero(action_cortado)!=len(action_cortado):
                        action_minimo = np.where(action_cortado==0) #cogemos los indices que tengan el valor maximo
                        rand = random.randint(0,len(action_minimo[0])-1)
                        action_relativo = action_minimo[0][rand] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
                        action=posicion_real(action_relativo, tablero.pentominos[0], orden)
                    else:
                        action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
                else:
                    action_maximo = np.where(action_cortado==np.amax(action_cortado)) #cogemos los indices que tengan el valor maximo
                    rand = random.randint(0,len(action_maximo[0])-1)
                    action_relativo = action_maximo[0][rand] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
                    action=posicion_real(action_relativo, tablero.pentominos[0], orden) #obtenemos el indice real ya que le anterior era el indice ralivo al array cortado
     
                action+=1 #Sumamos uno para contar en la tabla el hueco para la posicion 0
            
                next_state, penalty, done = tablero.colocar_siguiente(action,state) #Importante comprobar que la letra no este ya usada y que no quedan huecos para el reward
    
                if done or not tablero.pentominos:
                    faltantes=len(tablero.pentominos)+len(no_colocadas)
                    
                    qtable[state][action].update({key:50+penalty-10*faltantes})
                    if faltantes<=modo:
                        if modo_aux==0:
                            epsilon -= decay*epsilon
                            modo_aux=modo
                        else:
                            modo_aux-=1
                    
                else: 
                    if penalty==-1000:
                        
                        fila_aux[action].update({get_key(tablero):penalty})
                    
                        reward_completo = fila_aux #Buscamos en el estado
                        zona=rangos[letra_actual] #Obtenemos la zona de la table que afecta a la letra actual #Convertimos en array "aplaanamos"
                        reward_plano = np.squeeze(np.asarray(reward_completo)) #Convertimos en array "aplaanamos"
                        
                        reward_cortado_diccionario=reward_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
                        reward_cortado=[]
                        for dic in reward_cortado_diccionario:
                            if key in dic:
                                reward_cortado.append(dic[key])
                            else:
                                reward_cortado.append(0.0)
                                                        
                        reward_maximo = np.amax(reward_cortado)
                        if reward_maximo==-1000:
                            no_colocadas.append(letra_actual) #La ficha se ha probado en todas direcciones y no cabe en el tablero, asi que se pasa turno
                            tablero.pentominos.pop(0)
                    else:
                        reward_maximo=valor_maximo(qtable,rangos,tablero.pentominos[0], next_state,tablero)
                        qtable[state][action].update({key:penalty + gamma * reward_maximo})
                        
                state = next_state
                 
                steps += 1
                 
                if steps>limit or not tablero.pentominos:
                    done=True
            print(" ")
            print("epoch #", i+1, "/", epochs," .Step: ",steps)
            print(tablero)
            no_colocadas.append(tablero.pentominos)
            print(no_colocadas)
            print(tablero.piezas)
            print("Epsilon "+str(epsilon))
            print("\nDone in", steps, "steps".format(steps))
        with open(fichero,'w+') as f:
            for item in qtable:
                f.write(str(item))
                f.write("\n")
    return qtable
    

def valor_maximo(qtable,rangos,letra_actual, next_state,tablero):
    reward_completo = np.copy(qtable[next_state]) #Buscamos en el estado
#     print("Reward Completo "+str(reward_completo))
    zona=rangos[letra_actual] #Obtenemos la zona de la table que afecta a la letra actual #Convertimos en array "aplaanamos"
    reward_plano = np.squeeze(np.asarray(reward_completo)) #Convertimos en array "aplaanamos"
#     print("Reward Plano "+str(reward_plano))
#     print("Zona"+str(zona))
    reward_cortado_diccionario=reward_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
#     print("Reward cortado diccionarios"+str(reward_cortado_diccionario))
    reward_cortado=[]
    for dic in reward_cortado_diccionario:
        key=get_key(tablero)
        if key in dic:
            reward_cortado.append(dic[key])
        else:
            reward_cortado=[0]*(zona[1]+1-zona[0])
#     print("Reward cortado "+str(reward_cortado))
    
    reward_maximo = np.amax(reward_cortado) #buscamos el maximo, que seria la mejor opción de entre las opciones de accion
    if reward_maximo==-1000:
        reward_maximo=0
    return reward_maximo


def get_key(tablero):
    key=''
    for pieza in tablero.piezas:
        key+=str(pieza)
    return key
