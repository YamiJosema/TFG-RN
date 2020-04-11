# -*- coding: utf-8 -*-
import numpy
from neurolab import net
from neurolab import trans

def Perceptrones():
    perceptron = net.newp(minmax=[[0, 1], [0, 1]], cn=1)

    print(perceptron.inp_minmax) # rangos
    print(perceptron.co) # neuronas de salida
    print(perceptron.trainf) #funci�n de entrenamiento
    print(perceptron.errorf) # error
    capa = perceptron.layers[0] # capa oculta (posicion 0 en layers)
    print(capa.ci) # entradas de la capa oculta
    print(capa.cn) # numero de neuronas de la capa oculta
    print(capa.co) # salidas
    print(capa.np) # diccionario con los sesgos y los pesos de las conexiones de la capa
    
    entrada = numpy.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    objetivo = numpy.array([[0], [0], [0], [1]])
    
    print(perceptron.step([1, 1]))
    
    print(perceptron.sim(entrada))
    
    print(perceptron.errorf(objetivo, perceptron.sim(entrada)))
    
    pt = perceptron.train(entrada, objetivo)
    print(pt)
    
    print(perceptron.layers[0].np)
    print(perceptron.errorf(objetivo, perceptron.sim(entrada)))

def RedesHaciaDelante():
    funcion_sigmoide = trans.LogSig()
    red = net.newff(minmax=[[0, 1], [0, 1]], size=[2, 1], transf=[funcion_sigmoide]*2)
    
    print(red.inp_minmax) # rangos de los valores de entrada
    print(red.co)  # cuantas neuronas de salida
    print(red.trainf) # entrenamiento delta por defecto
    print(red.errorf) # error cuadrático u otro
    
    # Capa oculta
    capa_oculta = red.layers[0]
    print(capa_oculta.ci)
    print(capa_oculta.cn)
    print(capa_oculta.co)
    print(capa_oculta.np)
    
    # Capa de salida
    capa_de_salida = red.layers[1]
    print(capa_de_salida.ci) # num. entradas
    print(capa_de_salida.cn) # num. neuronas
    print(capa_de_salida.co) # num. salidas
    print(capa_de_salida.np) # sesgos y pesos
    
    entrada = numpy.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # bloque de entradas
    objetivo = numpy.array([[0], [1], [1], [0]])            # bloque de salidas esperadas
    print(red.sim(entrada))                                 # cálculo de salidas sin entrenamiento
    print(red.errorf(objetivo, red.sim(entrada)))           # error cometido en la salida 

def especie_lirio(array):
    m = max([(array[i],i) for i in range(3)])
    return m[1]

def ejercicio2():
    def rango(valores):
        return [min(valores),max(valores)]
    
    rangos = [rango(iris['Longitud sépalo']),
              rango(iris['Anchura sépalo']),
              rango(iris['Longitud pétalo']),
              rango(iris['Anchura pétalo'])]
    
    rediris = net.newff(minmax=rangos, size=[2, 3], transf=[trans.LogSig()]*2) # 1, 2, 3, 4
    for capa in rediris.layers:
        capa.initf = init.init_zeros                                             # 5
    rediris.trainf = train.train_gd                                              # 6
    rediris.errorf = error.SSE()                                                 # 7
    
    # print(entrada_entrenamiento.head(10))
    # print(objetivo_entrenamiento[:10])
    
    rediris.init()
    # Sesgos y pesos iniciales
    print(rediris.layers[0].np)
    print(rediris.layers[1].np)
    
    # Entrenamos
    rediris.train(entrada_entrenamiento, objetivo_entrenamiento, lr=0.01, epochs=1000, show=100, goal=0.001)
    
    # Sesgos y pesos al final
    print(rediris.layers[0].np)
    print(rediris.layers[1].np)
    
    # Error
    print(rediris.errorf(objetivo_entrenamiento, rediris.sim(entrada_entrenamiento)))


if __name__=="__main__":
    Perceptrones()