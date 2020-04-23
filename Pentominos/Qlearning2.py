# -*- coding: utf-8 -*-
import numpy as np
import time
import os
import sys
from Pentominos.Modelo import Tablero
from Pentominos.Utilidades import cargar_pentominos, rango_por_letra, posicion_real


if __name__=="__main__":
#     create environment
#     env=Env()
    
    orden = ["F","I","L","N","P","T","U","V","W","X","Y","Z"]
#     orden = ["I","X","U","Z","V","T","W","P","F","L","N","Y"]
    tablero = Tablero(8,8,orden)
    pentominos = cargar_pentominos()
    no_colocadas=[]
    
    rangos = rango_por_letra(orden)
    print(rangos)
    
    # Inicializamos la qtable a 0 
    # qtable[estado,accion]
    qtable = np.matrix(np.zeros([len(pentominos)+1,len(pentominos)+1]))
#     np.set_printoptions(threshold=sys.maxsize)
#     np.set_printoptions(threshold=np.inf)
    
    # hyperparameters
    epochs = 5 #epocas
    gamma = 0.4#0.1
    epsilon = 0.#0.08
    decay = 0.01
       
    limit=200 #pasos
       
    # training loop
    for i in range(epochs):
        state, penalty, done = tablero.reset(orden)
        steps = 0
       
        while not done:
            # act randomly sometimes to allow exploration
#             print("SIGUIENTE LETRA: "+tablero.pentominos[0])
            if np.random.uniform() < epsilon:
                action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
#                 print("La accion elegida es aleatoria: "+str(action))
            # if not select max action in Qtable (act greedy)
            else:
                #TODO convertir en un metodo para no reptir codigo
                action_completo = qtable[state] #Acciones para el estado
                action_plano = np.squeeze(np.asarray(action_completo)) #Convertimos en array "aplaanamos"
                zona=rangos[tablero.pentominos[0]] #rango que nos indica las acciones siguientes permitidas
#                 print(zona)
                action_cortado=action_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
#                 print(action_cortado)
                action_maximo = np.where(action_cortado==np.amax(action_cortado)) #cogemos los indices que tengan el valor maximo
                action_relativo = action_maximo[0][0] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
#                 print("Máximo relativo "+str(action_relativo))
                action=posicion_real(action_relativo, tablero.pentominos[0], orden) #obtenemos el indice real ya que le anterior era el indice ralivo al array cortado
#                 print("Posición Real "+str(action))
                
                action+=1 #Sumamos uno para contar en la tabla el hueco para la posici�n 0
#                 print("La accion elegida se saca de la tabla: "+str(action))
       
            # take action
#             print("Estado "+str(state))
#             print("Accion "+str(action))
            next_state, penalty, done = tablero.colocar_siguiente(action,state) #Importante comprobar que la letra no este ya usada y que no quedan huecos para el reward
#             print("Penalti "+str(penalty))
            
            # update qtable value with Bellman equation
            if not done:
                reward_completo = qtable[next_state]
                reward_plano = np.squeeze(np.asarray(reward_completo))
                zona=rangos[tablero.pentominos[0]] #TODO codigo repetido
                reward_cortado=reward_plano[zona[0]:zona[1]+1]
                reward_maximo = np.amax(reward_cortado)
                qtable[state,action] = (penalty + gamma * reward_maximo) if penalty>-1000 else penalty
            else:
                qtable[state,action]=100
                
#             print("Resultado")
#             print(qtable[state,action])
            
            # update state
            state = next_state
            
            if not done:
                #TODO convertir en un metodo para no reptir codigo
                action_completo = qtable[state] #Acciones para el estado
                action_plano = np.squeeze(np.asarray(action_completo)) #Convertimos en array "apalanamos"
                zona=rangos[tablero.pentominos[0]] #rango que nos indica las acciones siguientes permitidas
                action_cortado=action_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
                maximo=np.amax(action_cortado)
#                 print("PROBLEMAS?")
#                 print(action_cortado)
#                 print(maximo)
                if maximo==-1000: #La ficha se ha probado en todas direcciones y no cabe en el tablero, asi que se pasa turno
                    no_colocadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0) #TODO no modificar la variable del tablero para no perder puntuacion
               
            # count steps to finish game
            steps += 1
            
            if steps>limit or not tablero.pentominos:
                done=True
            
        # The more we learn, the less we take random actions
        epsilon -= decay*epsilon
           
        print(" ")
        print("epoch #", i+1, "/", epochs," .Step: ",steps)
        print(tablero)
        no_colocadas.append(tablero.pentominos)
        print(no_colocadas)
        print(tablero.piezas)
        print(tablero.fichas_colocadas)
        
        no_colocadas=[]
       
        print("\nDone in", steps, "steps".format(steps))
           
#         time.sleep(0.8)
    print(qtable)
