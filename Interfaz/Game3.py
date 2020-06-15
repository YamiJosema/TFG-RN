# -*- coding: utf-8 -*-
import pygame
from Pentominos.Formas import modelo
import numpy as np
import random
from Pentominos.Modelo import Tablero, Pentomino
from Pentominos.Qlearning2 import qlearning2
from Pentominos.Utilidades import Formas, cargar_pentominos, rango_por_letra, posicion_real
from Pentominos.Neuronales import red_neuronal, get_max
    
W_CUBO = 50
display_width = 1200
display_height = 700
FORMAS=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
VERDE=(0,255,0)
ROJO=(255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
AZUL = (0,0,255)
VIOLETA =(87,35,100)
GRIS = (105,105,105)
TRANSPARENTE=(0,0,0,0)
TURNOS = []
                

def board(tablero):
    for i in range(tablero.x):
        for j in range(tablero.y):
            if tablero.board[i][j]==0:
                cuadrado(i, j,VERDE)
            elif tablero.board[i][j]==1:
                cuadrado(i, j,ROJO)
            elif tablero.board[i][j]==2:
                cuadrado(i, j, AZUL)
            else:
                cuadrado(i, j, GRIS)
                    

def cuadrado(x,y,color):
    yc = 60+50*x+2*x
    xc = 52+50*y+2*y
    w=W_CUBO
    h=W_CUBO
    pygame.draw.rect(gameDisplay,color,[xc,yc,w,h])
    

def load_letras():
    f=pygame.image.load('images/botonF.png')
#     f=pygame.transform.scale(f,(100,100))
    i=pygame.image.load('images/botonI.png')
    l=pygame.image.load('images/botonL.png')
    n=pygame.image.load('images/botonN.png')
    p=pygame.image.load('images/botonP.png')
    t=pygame.image.load('images/botonT.png')
    u=pygame.image.load('images/botonU.png')
    v=pygame.image.load('images/botonV.png')
    w=pygame.image.load('images/botonW.png')
    x=pygame.image.load('images/botonX.png')
    y=pygame.image.load('images/botonY.png')
    z=pygame.image.load('images/botonZ.png')
    fpush=pygame.image.load('images/pushF.png')
    ipush=pygame.image.load('images/pushI.png')
    lpush=pygame.image.load('images/pushL.png')
    npush=pygame.image.load('images/pushN.png')
    ppush=pygame.image.load('images/pushP.png')
    tpush=pygame.image.load('images/pushT.png')
    upush=pygame.image.load('images/pushU.png')
    vpush=pygame.image.load('images/pushV.png')
    wpush=pygame.image.load('images/pushW.png')
    xpush=pygame.image.load('images/pushX.png')
    ypush=pygame.image.load('images/pushY.png')
    zpush=pygame.image.load('images/pushZ.png')
    foff=pygame.image.load('images/offF.png')
    ioff=pygame.image.load('images/offI.png')
    loff=pygame.image.load('images/offL.png')
    noff=pygame.image.load('images/offN.png')
    poff=pygame.image.load('images/offP.png')
    toff=pygame.image.load('images/offT.png')
    uoff=pygame.image.load('images/offU.png')
    voff=pygame.image.load('images/offV.png')
    woff=pygame.image.load('images/offW.png')
    xoff=pygame.image.load('images/offX.png')
    yoff=pygame.image.load('images/offY.png')
    zoff=pygame.image.load('images/offZ.png')
    
    letters=[('F',f),('I',i),('L',l),('N',n),('P',p),('T',t),('U',u),('V',v),('W',w),('X',x),('Y',y),('Z',z)]
    hoverl=[fpush,ipush,lpush,npush,ppush,tpush,upush,vpush,wpush,xpush,ypush,zpush]
    offl =[foff,ioff,loff,noff,poff,toff,uoff,voff,woff,xoff,yoff,zoff]
    
    return letters, hoverl, offl


def panel_letras(pulsadas):
    letters,_,offl = load_letras()
    x=540
    y=25
    column=0
    for letra in range(len(letters)):
        if letters[letra][0] not in pulsadas:
            gameDisplay.blit(letters[letra][1],(x,y))
        elif letters[letra][0] in pulsadas:
            gameDisplay.blit(offl[letra],(x,y))
        if column != 3:
            x=x+160
            column+=1
        else:
            x=540
            y=y+160
            column=0
    pygame.display.update()


# def letras(pulsadas, tablero):
#     mouse = pygame.mouse.get_pos()
#     click = pygame.mouse.get_pressed()
#     letters, hoverl, offl = load_letras()
#     x=540
#     y=25
#     column=0
#     for letra in range(len(letters)):
#         if letters[letra][0]==tablero.pentominos[0]:
#             gameDisplay.blit(offl[letra],(x,y))
#             vuelta=colocar_letra(letters[letra][0], tablero)
#             if not vuelta:
#                 pulsadas.append(letters[letra][0])
#             print(pulsadas)
#         elif letters[letra][0] not in pulsadas:
#             gameDisplay.blit(letters[letra][1],(x,y))
#         elif letters[letra][0] in pulsadas:
#             gameDisplay.blit(offl[letra],(x,y))
#         if column != 3:
#             x=x+160
#             column+=1
#         else:
#             x=540
#             y=y+160
#             column=0
            

# def comprobar_colocar_letra(pentomino, tablero):
#     pos_x,pos_y=tablero.comprobar_pentomino(pentomino)
#     if pos_x>0:     
#         mov_x=pos_x
#         mov_y=pos_y
#         forma = pentomino.modelo
#         for i in range(len(forma)):
#             for j in range(len(forma[0])):
#                 if forma[i][j]==1:
#                     if tablero.board[mov_x][mov_y]==0:
#                         if TURNOS[-1]==1:
#                             cuadrado(mov_x, mov_y,ROJO)
#                         else:
#                             cuadrado(mov_x, mov_y,AZUL)
#                 mov_y+=1
#             mov_y=pos_y
#             mov_x+=1
#     else:
#         print("Se queda fuera")
#     pygame.display.update() 
#     return pos_x,pos_y

def pintar_letra(opcion):
    forma = opcion[0].modelo
    mov_x=opcion[1]
    mov_y=opcion[2]
    for i in range(len(forma)):
        for j in range(len(forma[0])):
            if forma[i][j]==1:
                if tablero.board[mov_x][mov_y]==0:
                    if TURNOS[-1]==1:
                        cuadrado(mov_x, mov_y,VIOLETA)
                    else:
                        cuadrado(mov_x, mov_y,AZUL)
            mov_y+=1
        mov_y=opcion[2]
        mov_x+=1
    

def opciones(tablero,):
    rangos=rango_por_letra(FORMAS)
    rango=rangos[tablero.pentominos[0]]
    opciones=[]
#     print("Rango "+str(rango))
    for r in range(rango[0],rango[1]+1):
        pent=tablero.fichas[r-1]
        pentomino = Pentomino(pent[0],int(pent[1]),int(pent[2]))
#         print("Pentomino "+str(pentomino))
        x,y=tablero.comprobar_pentomino(pentomino)
#         print("("+str(x)+","+str(y)+")")
        if x!=-1:
            opciones.append([pentomino,x,y])
    return opciones
    

def colocar_letra(tablero, opciones):
    colocada = False
    posicionada = False
    r=0
    out=False
    replay=False
    while not colocada:
        p=opciones[r]
        if not posicionada:
            posicionada = True
            pintar_letra(p)
            teclas_escR()
            pygame.display.update()
            
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                if tecla == "return":
                    colocada=tablero.colocar_pentomino_2p(p[0],p[1],p[2],TURNOS[-1]) #jugador
                    tablero.buscar_huecos(TURNOS[-1])
                    if TURNOS[-1]==1:
                        TURNOS.append(2)
                    else:
                        TURNOS.append(1)
                    board(tablero)
                elif tecla== "d":
                    posicionada = False
                    r+=1
                    if r>=len(opciones):
                        r=0
                    board(tablero)
                elif tecla== "a":
                    posicionada = False
                    r-=1
                    if r<0:
                        r=len(opciones)-1
                    board(tablero)
                elif tecla=="escape":
                    out=True
                    colocada=True
                elif tecla=="r":
                    replay=True
                    colocada=True
    return p[0], replay, out
            

def display_text(texto, x, y, size, color):   
#     font = pygame.font.Font('resources/8-BIT WONDER.TTF',size)
    font = pygame.font.SysFont(None,size)
    textSurf = font.render(texto, True, color)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)
    
    
def get_puntuacion(tablero):
    p1=0
    p2=0
    for i in range(tablero.x):
        for j in range(tablero.y):
            if tablero.board[i][j]==1:
                p1+=10
            elif tablero.board[i][j]==-1:
                p1-=10
            elif tablero.board[i][j]==2:
                p2+=10
            elif tablero.board[i][j]==-2:
                p2-=10
    return p1, p2


def win(p1,p2):
    corona=pygame.image.load('images/corona.png')
    corona = pygame.transform.scale(corona, (50, 40))
    if p1>p2:
        gameDisplay.blit(corona,(display_width*0.06, display_height*0.81))
    elif p2>p1:
        gameDisplay.blit(corona,(display_width*0.66, display_height*0.81))
    elif p1==p2:
        pass
    

def teclas_escR():
    display_text("Reiniciar",display_width*0.47, display_height*0.79, 35, WHITE)
    display_text("Salir",display_width*0.57, display_height*0.79, 35, WHITE)
    esc=pygame.image.load('images/tecla_esc.png')
    r=pygame.image.load('images/tecla_r.png')
    r = pygame.transform.scale(r, (50, 50))
    gameDisplay.blit(r,(display_width*0.45, display_height*0.81))
    esc = pygame.transform.scale(esc, (50, 50))
    gameDisplay.blit(esc,(display_width*0.55, display_height*0.81))
            

def parar_reiniciar():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    replay=pygame.image.load('images/loop.png')
    stop=pygame.image.load('images/stop.png')
    replay = pygame.transform.scale(replay, (50, 50))
    gameDisplay.blit(replay,(display_width*0.45, display_height*0.81))
    stop = pygame.transform.scale(stop, (50, 50))
    gameDisplay.blit(stop,(display_width*0.55, display_height*0.81))
    if display_width*0.45+50>mouse[0]>display_width*0.45 and display_height*0.81+50>mouse[1]>display_height*0.81 and click[0]==1: #Replay
        return "Replay"
    if display_width*0.55+50>mouse[0]>display_width*0.55 and display_height*0.81+50>mouse[1]>display_height*0.81 and click[0]==1: #Stop
        return "Stop"
            
    
if __name__=="__main__":
    pygame.init()
    
    pulsadas=[]
    
    turno = random.randint(1,2)
    TURNOS.append(random.randint(1,2))
    
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Prueba1')
    clock = pygame.time.Clock()
    
    gameDisplay.fill(BLACK)
    tablero = Tablero(8,8, FORMAS)
    board(tablero)
    
#     qtable = qlearning2(tablero.copy())
    red=red_neuronal()

    out = False
    replay=False
    
    p1,p2=0,0
    print("COMIENZA EL JUEGO")
    
    while not out:
        
        i,j=tablero.siguiente_zero()
        p1, p2 = get_puntuacion(tablero)
        pygame.draw.rect(gameDisplay,BLACK,[0, display_height*0.85-60,display_width,100])
        display_text("P1:"+str(p1),display_width*0.2, display_height*0.85, 100, WHITE)
        display_text("P2:"+str(p2),display_width*0.8, display_height*0.85, 100, WHITE)
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                out = True
        if i!=-1:
            panel_letras(pulsadas)
            if TURNOS[-1]==1:
                print("Turno jugador 1")
                op=opciones(tablero)
                while not op:
                    print("Descartamos la "+tablero.pentominos[0])
                    pulsadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                    panel_letras(pulsadas)
                ficha_colocada,replay,out=colocar_letra(tablero,op)
                
                pulsadas.append(ficha_colocada.letra)
                TURNOS.append(2)
                pygame.display.update()
#                 print("Ficha: "+str(tablero.movimientos[-1][0]))
                print(tablero)
            else:
                print("Turno jugador 2")
                op=opciones(tablero)
#                 print("Opciones "+str(op))
                while not op:
                    print("Descartamos la "+tablero.pentominos[0])
                    pulsadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                    panel_letras(pulsadas)
                
                valida=False
                cambio=False
                
                while not cambio:
                    entrada=[] 
                    aux=[0]*63
                    if not tablero.movimientos:
                        state=0
                        entrada.append(aux)
                        
                    else:
                        ultimo_movimiento=tablero.movimientos[-1][0]
                        estado=tablero.fichas.index(ultimo_movimiento)
                        print(estado)
                        aux[estado]=1
                        print(aux)
                        entrada.append(aux)
                    print(entrada)
                    solucion=red.sim(entrada)
                    
                    old_action=-1
                    while not valida:
                        state,action=get_max(entrada[0],solucion[0])
        #                 action+=1
                        print("Estado, accion: ("+str(state)+", "+str(action)+")")
                        
                        pent = tablero.fichas[action]#Comprobar que entra, si no entra, elegimos otro de los m�ximos
                        print("Ficha: "+str(pent))
                        pentomino=Pentomino(pent[0],int(pent[1]),int(pent[2]))
                        
                        x,y=tablero.comprobar_pentomino(pentomino)
                            
                        if x==-1:
                            print("No es valida")
                            solucion[0][action]=-1000
                            if old_action==action:
                                valido=True
                                pulsadas.append(tablero.pentominos[0])
                                tablero.pentominos.pop(0)
#                                 op=opciones(tablero)
                                panel_letras(pulsadas)
                            else:
                                old_action=action
                        else:
                            print("Es valida")
                            valida=True
                            cambio=True    
                                
                        tablero.colocar_pentomino_2p(pentomino, x, y, TURNOS[-1])
                        teclas_escR()
                        pulsadas.append(pentomino.letra)
                        tablero.buscar_huecos(TURNOS[-1])
                        print(tablero)
                        board(tablero)
                        TURNOS.append(1)
                        pygame.display.update()
        elif i==-1:
            panel_letras(pulsadas)
            win(p1,p2)
            pr=parar_reiniciar()
            if pr=="Replay":
                tablero=Tablero(8,8,FORMAS)
                pulsadas=[]
                board(tablero)
                turno = random.randint(1,2)
                TURNOS.append(turno)
            elif pr=="Stop":
                out=True
        if replay:
            replay=False
            tablero=Tablero(8,8,FORMAS)
            pulsadas=[]
            board(tablero)
            turno = random.randint(1,2)
            TURNOS.append(turno)
        pygame.display.update()
        
        clock.tick(30)
        
#     print(tablero)
#     print(tablero.movimientos)
    pygame.quit()
    quit()