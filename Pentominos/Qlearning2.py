# -*- coding: utf-8 -*-
import numpy as np
import sys
import random
from Pentominos.Modelo import Tablero
from Pentominos.Utilidades import cargar_pentominos, rango_por_letra, posicion_real


def qlearning2(tablero, epochs=100, gamma=0.4, epsilon=0.3, decay=0.01, limit=200):
    orden = tablero.pentominos
    pentominos = cargar_pentominos(orden)
    no_colocadas=[]
    rangos = rango_por_letra(orden)
    
    qtable = np.matrix(np.zeros([len(pentominos)+1,len(pentominos)+1]))
    np.set_printoptions(threshold=sys.maxsize)
    
    for i in range(epochs):
        state, penalty, done = tablero.reset(orden)
        steps = 0
       
        while not done:
            # act randomly sometimes to allow exploration
            letra_actual=tablero.pentominos[0]

            if np.random.uniform() < epsilon:
                action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
            # if not select max action in Qtable (act greedy)
            else:
                #TODO convertir en un metodo para no reptir codigo
                action_completo = qtable[state] #Acciones para el estado
                action_plano = np.squeeze(np.asarray(action_completo)) #Convertimos en array "aplaanamos"
                zona=rangos[tablero.pentominos[0]] #rango que nos indica las acciones siguientes permitidas
                action_cortado=action_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
                action_maximo = np.where(action_cortado==np.amax(action_cortado)) #cogemos los indices que tengan el valor maximo
                rand = random.randint(0,len(action_maximo[0])-1)
                action_relativo = action_maximo[0][rand] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
                action=posicion_real(action_relativo, tablero.pentominos[0], orden) #obtenemos el indice real ya que le anterior era el indice ralivo al array cortado

                action+=1 #Sumamos uno para contar en la tabla el hueco para la posici�n 0
       
            # take action
            next_state, penalty, done = tablero.colocar_siguiente(action,state) #Importante comprobar que la letra no este ya usada y que no quedan huecos para el reward

            # update qtable value with Bellman equation
            if done or not tablero.pentominos:
                qtable[state,action]=100+penalty
            else:
                reward_maximo=valor_maximo(qtable,rangos,letra_actual, next_state)
                while reward_maximo==-1000:
                    no_colocadas.append(letra_actual) #La ficha se ha probado en todas direcciones y no cabe en el tablero, asi que se pasa turno
                    tablero.pentominos.pop(0) #TODO no modificar la variable del tablero para no perder puntuacion
                    if not tablero.pentominos:
                        break
                    letra_actual=tablero.pentominos[0]
                    reward_maximo=valor_maximo(qtable,rangos,letra_actual, next_state)
                qtable[state,action] = (penalty + gamma * reward_maximo) if penalty>-1000 else penalty
                
                
            # update state
            state = next_state
            
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
    
    return qtable
    

def valor_maximo(qtable,rangos,letra_actual, next_state):
    reward_completo = qtable[next_state] #Buscamos en el estado
#     print("Reward Completo "+str(reward_completo))
    zona=rangos[letra_actual] #Obtenemos la zona de la table que afecta a la letra actual #Convertimos en array "aplaanamos"
    reward_plano = np.squeeze(np.asarray(reward_completo)) #Convertimos en array "aplaanamos"
    reward_cortado=reward_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
#     print("Reward Cortado "+str(reward_cortado))
    reward_maximo = np.amax(reward_cortado) #buscamos el maximo, que seria la mejor opción de entre las opciones de accion
    return reward_maximo


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
    qtable = np.matrix(np.zeros([len(pentominos)+1,len(pentominos)+1]))
    np.set_printoptions(threshold=sys.maxsize)
#     np.set_printoptions(threshold=np.inf)
     
    # hyperparameters
    epochs = 10000 #epocas
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
            last_state=state
 
            if np.random.uniform() < epsilon:
                action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
#                 print("La accion elegida es aleatoria: "+str(action)+"("+letra_actual+")")
            # if not select max action in Qtable (act greedy)
            else:
                #TODO convertir en un metodo para no reptir codigo
                action_completo = fila_aux#qtable[state] #Acciones para el estado
                action_plano = np.squeeze(np.asarray(action_completo)) #Convertimos en array "aplaanamos"
                zona=rangos[tablero.pentominos[0]] #rango que nos indica las acciones siguientes permitidas
#                 print(zona)
                action_cortado=action_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
#                 print(action_cortado)
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
                qtable[state,action]=100-10*faltantes
                if faltantes<=1:
                    epsilon -= decay*epsilon
            else: 
                if penalty==-1000:
                    fila_aux[0][action]=penalty
                    
                    reward_completo = fila_aux #Buscamos en el estado
                    zona=rangos[letra_actual] #Obtenemos la zona de la table que afecta a la letra actual #Convertimos en array "aplaanamos"
                    reward_plano = np.squeeze(np.asarray(reward_completo)) #Convertimos en array "aplaanamos"
                    reward_cortado=reward_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones
                    reward_maximo = np.where(reward_cortado==np.amax(reward_cortado))
#                     print("Trozo cortado de la tabla "+str(reward_cortado))
#                     print("Maximos del trozo cortado "+str(reward_maximo[0]))
                    if len(reward_cortado)==len(reward_maximo[0]):
                        no_colocadas.append(letra_actual) #La ficha se ha probado en todas direcciones y no cabe en el tablero, asi que se pasa turno
                        tablero.pentominos.pop(0) #TODO no modificar la variable del tablero para no perder puntuacion

                else:
                    reward_maximo=valor_maximo(qtable,rangos,tablero.pentominos[0], next_state)  #TODO
#                     print("Rewar Maximo para el gamma: "+str(reward_maximo))
                    qtable[state,action] = (penalty + gamma * reward_maximo)
                 
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
#     print(qtable)
