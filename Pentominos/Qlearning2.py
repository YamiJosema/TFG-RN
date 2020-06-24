# -*- coding: utf-8 -*-
import numpy as np
import sys
import random
import os
from Pentominos.Modelo import Tablero
from Pentominos.Utilidades import cargar_pentominos, rango_por_letra, posicion_real
from numpy import float32


def qlearning2(tablero, modo=0, epochs=40000, gamma=0.4, epsilon=0.95, decay=0.001, limit=200):
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


if __name__=="__main__":
#     create environment
#     env=Env()
    
    orden = ["F","I","L","N","P","T","U","V","W","X","Y","Z"]
#     orden = ["I","X","U","Z","V","T","W","P","F","L","N","Y"]
    tablero = Tablero(8,8,orden)
    pentominos = cargar_pentominos(orden)
    no_colocadas=[]
     
    rangos = rango_por_letra(orden)
    print(rangos)
     
    # Inicializamos la qtable a 0 
    # qtable[estado,accion]
    qtable=[[{} for i in range(len(pentominos)+1)] for j in range(len(pentominos)+1)]
    
#     qtable = np.matrix(np.zeros([len(pentominos)+1,len(pentominos)+1]))
#     np.set_printoptions(threshold=sys.maxsize)
#     np.set_printoptions(threshold=np.inf)
     
    # hyperparameters
    epochs = 1000 #epocas
    gamma = 0.4#0.1
    epsilon = 0.9#0.08
    decay = 0.01
        
    limit=200 #pasos
        
    # training loop
    for i in range(epochs):
        state, penalty, done = tablero.reset(orden)
        steps = 0
        
        fila_aux=[]
        last_state=state
        while not done:
            # act randomly sometimes to allow exploration
#             print("LETRA ACTUAL: "+tablero.pentominos[0])
            letra_actual=tablero.pentominos[0]
#             print("Anterior estado "+str(last_state))
#             print("EStado actual "+str(state))
            if last_state!=state or not np.any(fila_aux):
                fila_aux=np.copy(qtable[state])
#                 print("Fila del estado" +str(fila_aux))
            last_state=state
 
            if np.random.uniform() < epsilon:
                action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
#                 print("La accion elegida es aleatoria: "+str(action)+"("+letra_actual+")")
            # if not select max action in Qtable (act greedy)
            else:
                #TODO convertir en un metodo para no reptir codigo
                action_completo = fila_aux#qtable[state] #Acciones para el estado
                action_plano = np.squeeze(np.asarray(action_completo)) #Convertimos en array "aplaanamos"
#                 print("Action Plano "+str(action_plano))
                zona=rangos[tablero.pentominos[0]] #rango que nos indica las acciones siguientes permitidas
#                 print("Zona"+str(zona))
                action_cortado_diccionario=action_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
#                 print("Action cortado diccionarios"+str(action_cortado_diccionario))
                action_cortado=[]
                for dic in action_cortado_diccionario:
                    key=''
                    for pieza in tablero.piezas:
                        key+=str(pieza)
                    if key in dic:
                        action_cortado.append(dic[key])
                    else:
                        action_cortado.append(0)
#                 print("Action cortado "+str(action_cortado))
                action_maximo = np.where(action_cortado==np.amax(action_cortado)) #cogemos los indices que tengan el valor maximo
#                 print("Máximo "+str(action_maximo[0]))
                rand = random.randint(0,len(action_maximo[0])-1)
                action_relativo = action_maximo[0][rand] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
#                 print("Máximo relativo "+str(action_relativo))
                action=posicion_real(action_relativo, tablero.pentominos[0], orden) #obtenemos el indice real ya que le anterior era el indice ralivo al array cortado
#                 print("Posición Real "+str(action))
#                 print("La accion elegida se saca de la tabla: "+str(action))
 
            action+=1 #Sumamos uno para contar en la tabla el hueco para la posici�n 0
        
            # take action
#             print("Estado "+str(state))
#             print("Accion "+str(action))
            next_state, penalty, done = tablero.colocar_siguiente(action,state) #Importante comprobar que la letra no este ya usada y que no quedan huecos para el reward
#             print("Penalti "+str(penalty))
 
            # update qtable value with Bellman equation
            # Consideramos que el tablero esta completo y lo situamos como puntuación máxima
            if done or not tablero.pentominos:
                faltantes=len(tablero.pentominos)+len(no_colocadas)
                key=''
                for pieza in tablero.piezas:
                    key+=str(pieza)
                qtable[state][action].update({key:50+penalty-10*faltantes})
                if faltantes<=1:
                    epsilon -= decay*epsilon
            else: 
                if penalty==-1000:
                    fila_aux[action].update({get_key(tablero):penalty})
                    
                    reward_completo = fila_aux #Buscamos en el estado
                    zona=rangos[letra_actual] #Obtenemos la zona de la table que afecta a la letra actual #Convertimos en array "aplaanamos"
                    reward_plano = np.squeeze(np.asarray(reward_completo)) #Convertimos en array "aplaanamos"
                    
                    reward_cortado_diccionario=reward_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
                    reward_cortado=[]
                    for dic in reward_cortado_diccionario:
                        key=get_key(tablero)
                        if key in dic:
                            reward_cortado.append(dic[key])
                        else:
                            reward_cortado.append(0)
                    
                    reward_maximo = np.amax(reward_cortado)
#                     print("Trozo cortado de la tabla "+str(reward_cortado))
#                     print("Maximos del trozo cortado "+str(reward_maximo[0]))
                    if reward_maximo==-1000:
                        no_colocadas.append(letra_actual) #La ficha se ha probado en todas direcciones y no cabe en el tablero, asi que se pasa turno
                        tablero.pentominos.pop(0) #TODO no modificar la variable del tablero para no perder puntuacion

                else:
                    reward_maximo=valor_maximo(qtable,rangos,tablero.pentominos[0], next_state,tablero)  #TODO
#                     print("Rewar Maximo para el gamma: "+str(reward_maximo))
                    key=''
                    for pieza in tablero.piezas:
                        key+=str(pieza)
                    qtable[state][action].update({key:penalty + gamma * reward_maximo})
                 
#             print("Resultado")
#             print(qtable[state,action])
             
            # update state
            state = next_state
             
            # count steps to finish game
            steps += 1
             
            if steps>limit or not tablero.pentominos:
                done=True
             
        # The more we learn, the less we take random actions
            
            
        print(" ")
        print("epoch #", i+1, "/", epochs," .Step: ",steps)
        print(tablero)
        no_colocadas.append(tablero.pentominos)
        print(no_colocadas)
        print(tablero.piezas)
        print("Epsilon "+str(epsilon))
         
        no_colocadas=[]
        
        print("\nDone in", steps, "steps".format(steps))
        
#         time.sleep(0.8)
    print(qtable)
