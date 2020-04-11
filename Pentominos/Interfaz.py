# -*- coding: utf-8 -*-
import csv
import os 
from Main import cargar_pentominos, get_pentominos, red_neuronal, crear_pentominos_csv
from Modelo import *
from Formas import modelo

from Pentominos.Main import get_max


Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
Pentominos=[]

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
    
    print tablero.colocar_sin_superposicion(mano[0],0,0)
    print tablero.colocar_sin_superposicion(mano[1],4,0)
    print tablero
    print tablero.pentominos
    print tablero.todos_usados()
    
    
def cargar_pentominos():
    if os.path.isfile('csv/pentominos.csv')==False:
        crear_pentominos_csv()
    
    with open('csv/pentominos.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            Pentominos.append(row)
    

def pedir_ficha(tablero):
    print tablero.pentominos
    letra = raw_input("Selecciona pentomino disponible\n") #Solo input en python 3
    while letra not in tablero.pentominos:
        print tablero.pentominos
        letra = raw_input("Incorrecto. Selecciona solo pentominos disponibles\n") #Solo input en python 3
    giro = raw_input("Selecciona si quieres rotar la ficha (0 1 2 3)\n") #Solo input en python 3
    while giro!="0" and giro!="1" and giro!="2" and giro!="2":
        giro = raw_input("Incorrecto. Selecciona uno de los valores posible (0 1 2 3)\n") #Solo input en python 3
    giro = int(giro)
    invertido = raw_input("Selecciona si quieres invertir la ficha (0 1)\n") #Solo input en python 3
    while invertido!="0" and invertido!="1":
        invertido = raw_input("Incorrecto, 0 1\n") #Solo input en python 3
    invertido = int(invertido)
    
    pentomino = Pentomino(letra, giro, invertido)
    return pentomino


def ficha_ia(red, tablero):
    
    aux=["0"]*12
    aux[0]="1"
    aux[4]="26"
    aux=[aux]
    print aux
    solucion = red.sim(aux)
    ficha=get_max(solucion[0])
    ficha = Pentominos[int(ficha)]
    pent_ia=Pentomino(ficha[0], int(ficha[1]), int(ficha[1]))
    print pent_ia
    while pent_ia not in tablero.pentominos:
        aux=["0"]*12
        aux[0]="1"
        aux=[aux]
        solucion = red.sim(aux)
        ficha=get_max(solucion[0])
        ficha = Pentominos[int(ficha)]
        pent_ia=Pentomino(ficha[0], int(ficha[1]), int(ficha[1]))
    return pent_ia


def introduciendo_letras(red):
    cargar_pentominos()
    tablero = Tablero(8,8)
    for _ in range(4):
        print "--------------Comienzo--------------"
        print tablero
        
        print "--------------Movimiento jugador--------------"
        pentomino = pedir_ficha(tablero)
        colocado=tablero.colocar_siguiente(pentomino)
        print tablero
        
        print "--------------Movimiento IA--------------"
        pent_ia=ficha_ia(red, tablero)
        colocado=tablero.colocar_siguiente(pent_ia)
            
        print tablero
    

if __name__=="__main__":
    red = red_neuronal()
    introduciendo_letras(red)
