# -*- coding: utf-8 -*-
import csv
import os 
import random 
import numpy as np
from Pentominos.Main import cargar_pentominos, get_pentominos
from Pentominos.Modelo import *
from Pentominos.Formas import modelo

import pandas
import array


Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"]

def inicio(x,y,cartas):
    cargar_pentominos()
    
    tablero = Tablero(x,y)
    mano = []
    while cartas>0:
        index = random.randint(0, len(tablero.pentominos)-1)
        rotacion = random.randint(0,3)
        invertido = random.randint(0,1)
        forma = [tablero.pentominos[index],str(rotacion),str(invertido)]
        if forma in get_pentominos():
            pentomino = Pentomino(tablero.pentominos[index], rotacion, invertido)
            mano.append(pentomino)
            cartas-=1
        
    
    print "MANO:"
    for m in mano:
        print m
        print "\n"
#     print tablero
    
    
    print tablero.colocar_sin_superposicion(mano[0],1,5)
    print tablero.colocar_sin_superposicion(mano[1],5, 5)
    print tablero
    print tablero.pentominos
    print tablero.todos_usados()
    

if __name__=="__main__":
    inicio(8,8,5)