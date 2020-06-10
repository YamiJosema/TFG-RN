# -*- coding: utf-8 -*-
import pandas

from neurolab import init
from neurolab import trans
from neurolab import train
from neurolab import error
from neurolab import net
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

def especie_lirio(array):
    m = max([(array[i],i) for i in range(3)])
    return m[1]

def rango(valores):
    return [min(valores),max(valores)]

def rendimiento_red (red):
    diferencias = [(especie_lirio(a)-b) for (a,b) in zip(red.sim(entrada_prueba),objetivo_prueba)]
    aciertos = len([d for d in diferencias if d == 0])
    return aciertos/objetivo_prueba.shape[0]



if __name__=="__main__":
    iris = pandas.read_csv('iris.csv', header=None, names=['Longitud sépalo', 'Anchura sépalo','Longitud pétalo', 'Anchura pétalo','Especie'])
    iris.head(10)  # Diez primeros ejemplos
    
    ###### try: # para la versi�n antigua de sklearn: 
    ######     from sklearn.cross_validation import train_test_split, cross_val_score
    ###### except: # Para la versi�n nueva:
    ######     from sklearn.model_selection import train_test_split, cross_val_score
    
    
    le = preprocessing.LabelEncoder()   # Creamos codificador de etiquetas
    iris['Especie'] = le.fit_transform(iris['Especie']) # Codifica cada valor para Especie
    
    # Divido el conjunto iris de dos: el de entrenamiento es el 33% de los datos
    iris_entrenamiento, iris_prueba = train_test_split(
        iris, test_size=.33, random_state=2346523,
        stratify=iris['Especie'])
    
    ohe = preprocessing.OneHotEncoder(sparse = False) # Otro codificador que pone 1 en la coord. de la especie
    entrada_entrenamiento = iris_entrenamiento.iloc[:, :4] # todas las filas y 4 columnas
    objetivo_entrenamiento = ohe.fit_transform(iris_entrenamiento['Especie'].values.reshape(-1, 1))# matriz de una columna y tantas filsa como necesite
    entrada_prueba = iris_prueba.iloc[:, :4 ] # todas las filas, de las 4 columnas primeras
    objetivo_prueba = iris_prueba['Especie'] #Columna Especie
    
    print ("ENTRADA ENTRENAMIENTO")
    print(entrada_entrenamiento.head(10))
    print(entrada_entrenamiento.ndim)
    print("OBJETIVO ENTRENAMIENTO")
    print(objetivo_entrenamiento[:10])
    
    print(entrada_prueba.head(10))
    print(objetivo_prueba.head(10))
    
    rangos = [rango(iris['Longitud sépalo']),rango(iris['Anchura sépalo']),rango(iris['Longitud pétalo']),rango(iris['Anchura pétalo'])]
    
    print("Rangos "+str(rangos))
    
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
    
    print(entrada_entrenamiento)
    print(objetivo_entrenamiento)
    # Entrenamos
    rediris.train(entrada_entrenamiento, objetivo_entrenamiento, lr=0.01, epochs=1000, show=100, goal=0.001)
    
    # Sesgos y pesos al final
    print(rediris.layers[0].np)
    print(rediris.layers[1].np)
    
    # Error
    print(rediris.errorf(objetivo_entrenamiento, rediris.sim(entrada_entrenamiento)))
    
    
    rendimiento_red(rediris)

    # Caso 1: Tres neuronas en la capa oculta
    
    rediris1 = net.newff(minmax=rangos, size=[3, 3], transf=[trans.LogSig()]*2)
    for capa in rediris1.layers:
        capa.initf = init.init_zeros
    rediris1.trainf = train.train_gd
    rediris1.errorf = error.SSE()
    
    rediris1.init()
    rediris1.train(entrada_entrenamiento, objetivo_entrenamiento, lr=0.01, epochs=1000, show=100, goal=0.001)
    print(rediris1.errorf(objetivo_entrenamiento, rediris1.sim(entrada_entrenamiento)))
    rendimiento_red(rediris1)
    
    print ("-----------")
    print (rediris1.sim(entrada_entrenamiento))