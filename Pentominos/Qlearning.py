import numpy as np
import time
import os
from Pentominos.Modelo import Tablero
from Pentominos.Utilidades import cargar_pentominos


def qlearning(tablero,qtable=False):
#     tablero = Tablero(8,8)
    if not qtable:
        pentominos = cargar_pentominos()
        qtable = np.random.rand(len(pentominos)*11*12+1,len(pentominos)).tolist()
    
    epochs =100
    gamma = 0.2#0.1
    epsilon = 0.2#0.08
    decay = 0.1
    
    limit=200
    
    for i in range(epochs):
        state, reward, done = tablero.reset()
        steps = 0
    
        while not done:
            steps += 1
    
            if np.random.uniform() < epsilon:
                action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
            else:
                action = qtable[state].index(max(qtable[state]))
            next_state, reward, done = tablero.colocar_siguiente(action,state) #Importante comprobar que la letra no este ya usada y que no quedan huecos para el reward
    
            qtable[state][action] = (reward + gamma * max(qtable[next_state])) if reward>=-5 else reward
            
            state = next_state
            
            if steps>limit:
                done=True

        epsilon -= decay*epsilon
        
        print(" ")
        print("epoch #", i+1, "/", epochs," .Step: ",steps)
        print(tablero)
        print(tablero.pentominos)
        print(tablero.piezas)
    
    return qtable
        

if __name__=="__main__":
#     create environment
#     env=Env()
    tablero = Tablero(8,8)
    pentominos = cargar_pentominos()
     
    # QTable : contains the Q-Values for every (state,action) pair
    qtable = np.random.rand(len(pentominos)*11*12+1,len(pentominos)).tolist()
     
    # hyperparameters
    epochs =200
    gamma = 0.2#0.1
    epsilon = 0.2#0.08
    decay = 0.1
     
    limit=200
     
    # training loop
    for i in range(epochs):
        state, reward, done = tablero.reset()
        steps = 0
     
        while not done:
#             os.system('cls')
#             print("epoch #", i+1, "/", epochs," .Step: ",steps)
#             print("El estado es: "+str(state))
#             print(tablero)
#             print(tablero.pentominos)
#             env.render() Coloca el O donde esta
#             time.sleep(0.05)
     
            # count steps to finish game
            steps += 1
     
            # act randomly sometimes to allow exploration
            if np.random.uniform() < epsilon:
                action=tablero.ficha_aleatoria() #Usamos colocar random para poner una ficha aleatoria
            # if not select max action in Qtable (act greedy)
            else:
                action = qtable[state].index(max(qtable[state]))
     
#             print("La accion elegida es: "+str(action))
            # take action
            next_state, reward, done = tablero.colocar_siguiente(action,state) #Importante comprobar que la letra no este ya usada y que no quedan huecos para el reward
     
            # update qtable value with Bellman equation
            qtable[state][action] = (reward + gamma * max(qtable[next_state])) if reward>=-5 else reward
             
            # update state
            state = next_state
             
            if steps>limit:
                done=True
             
        # The more we learn, the less we take random actions
        epsilon -= decay*epsilon
         
        print(" ")
        print("epoch #", i+1, "/", epochs," .Step: ",steps)
        print(tablero)
        print(tablero.pentominos)
        print(tablero.piezas)
     
        print("\nDone in", steps, "steps".format(steps))
         
#         time.sleep(0.8)
#     print(qtable)
