import numpy as np


def separacion():
    tres_x_tres=["F","P","T","U","V","W","X","Z"]
    dos_x_cuatro=["L","N","Y"]
    dos_x_tres=["P","U"]
    uno_x_cinco=["I"]
    
    return tres_x_tres, dos_x_cuatro, dos_x_tres, uno_x_cinco


def F():
    return np.array([[0,1,1],[1,1,0],[0,1,0]])
def I():
    return np.array([[1],[1],[1],[1],[1]])
def L():
    return np.array([[1,0],[1,0],[1,0],[1,1]])
def N():
    return np.array([[0,1],[1,1],[1,0],[1,0]])
def P():
    return np.array([[0,1],[1,1],[1,1]])
def T():
    return np.array([[1,1,1],[0,1,0],[0,1,0]])
def U():
    return np.array([[1,0,1],[1,1,1]])
def V():
    return np.array([[1,0,0],[1,0,0],[1,1,1]])
def W():
    return np.array([[1,0,0],[1,1,0],[0,1,1]])
def X():
    return np.array([[0,1,0],[1,1,1],[0,1,0]])
def Y():
    return np.array([[0,1],[1,1],[0,1],[0,1]])
def Z():
    return np.array([[1,1,0],[0,1,0],[0,1,1]])

def modelo(letra):
    switcher={
        "F":F,
        "I":I,
        "L":L,
        "N":N,
        "P":P,
        "T":T,
        "U":U,
        "V":V,
        "W":W,
        "X":X,
        "Y":Y,
        "Z":Z
    }
    func = switcher.get(letra, lambda: "Forma invalida")
    return func()
