# -*- coding: utf-8 -*-
import pygame
import numpy as np
import random
from Pentominos.Modelo import Tablero, Pentomino
from Pentominos.Qlearning2 import qlearning2
from Pentominos.Utilidades import rango_por_letra, posicion_real
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
                

def board(tablero,gameDisplay):
    for i in range(tablero.x):
        for j in range(tablero.y):
            if tablero.board[i][j]==0:
                cuadrado(i, j,VERDE,gameDisplay)
            elif tablero.board[i][j]==1:
                cuadrado(i, j,ROJO,gameDisplay)
            elif tablero.board[i][j]==2:
                cuadrado(i, j, AZUL,gameDisplay)
            else:
                cuadrado(i, j, GRIS,gameDisplay)
                    

def cuadrado(x,y,color, gameDisplay):
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
    fnot=pygame.image.load('images/notF.png')
    inot=pygame.image.load('images/notI.png')
    lnot=pygame.image.load('images/notL.png')
    nnot=pygame.image.load('images/notN.png')
    pnot=pygame.image.load('images/notP.png')
    tnot=pygame.image.load('images/notT.png')
    unot=pygame.image.load('images/notU.png')
    vnot=pygame.image.load('images/notV.png')
    wnot=pygame.image.load('images/notW.png')
    xnot=pygame.image.load('images/notX.png')
    ynot=pygame.image.load('images/notY.png')
    znot=pygame.image.load('images/notZ.png')
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
    notl=[fnot,inot,lnot,nnot,pnot,tnot,unot,vnot,wnot,xnot,ynot,znot]
    offl =[foff,ioff,loff,noff,poff,toff,uoff,voff,woff,xoff,yoff,zoff]
    
    return letters, notl, offl


def panel_letras(pulsadas,descartadas, gameDisplay):
    letters,notl,offl = load_letras()
    x=540
    y=25
    column=0
    for letra in range(len(letters)):
        if letters[letra][0] in pulsadas:
            gameDisplay.blit(offl[letra],(x,y))
        elif letters[letra][0] in descartadas:
            gameDisplay.blit(notl[letra],(x,y))
        else:
            gameDisplay.blit(letters[letra][1],(x,y))
        if column != 3:
            x=x+160
            column+=1
        else:
            x=540
            y=y+160
            column=0
            

def pintar_letra(opcion,tablero, gameDisplay):
    forma = opcion[0].modelo
    mov_x=opcion[1]
    mov_y=opcion[2]
    for i in range(len(forma)):
        for j in range(len(forma[0])):
            if forma[i][j]==1:
                if tablero.board[mov_x][mov_y]==0:
                    cuadrado(mov_x, mov_y,VIOLETA, gameDisplay)
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
    

def colocar_letra(tablero, opciones,gameDisplay):
    colocada = False
    posicionada = False
    r=0
    out=False
    replay=False
    while not colocada:
        p=opciones[r]
        if not posicionada:
            posicionada = True
            pintar_letra(p,tablero,gameDisplay)
            teclas_escR(gameDisplay)
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
                    board(tablero,gameDisplay)
                elif tecla== "d":
                    posicionada = False
                    r+=1
                    if r>=len(opciones):
                        r=0
                    board(tablero,gameDisplay)
                elif tecla== "a":
                    posicionada = False
                    r-=1
                    if r<0:
                        r=len(opciones)-1
                    board(tablero,gameDisplay)
                elif tecla=="escape":
                    out=True
                    colocada=True
                elif tecla=="r":
                    replay=True
                    colocada=True
    return p[0], replay, out
            

def display_text(texto, x, y, size, color,gameDisplay):   
#     font = pygame.font.Font('resources/8-BIT WONDER.TTF',size)
    font = pygame.font.SysFont(None,size) #https://programtalk.com/python-examples/pygame.font.SysFont/
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


def win(p1,p2,gameDisplay):
    if p1!=p2:
        corona=pygame.image.load('images/corona.png')
        corona = pygame.transform.scale(corona, (70, 70))
        if p1>p2:
            gameDisplay.blit(corona,(display_width*0.04, display_height*0.79))
        elif p2>p1:
            gameDisplay.blit(corona,(display_width*0.64, display_height*0.79))
    elif p1==p2:
        empate=pygame.image.load('images/empate.png')
        empate = pygame.transform.scale(empate, (80,51))
        gameDisplay.blit(empate,(display_width*0.03, display_height*0.81))
        gameDisplay.blit(empate,(display_width*0.63, display_height*0.81))
    

def teclas_escR(gameDisplay):
    display_text("Reiniciar",display_width*0.47, display_height*0.79, 35, WHITE,gameDisplay)
    display_text("Atrás",display_width*0.57, display_height*0.79, 35, WHITE,gameDisplay)
    esc=pygame.image.load('images/tecla_esc.png')
    r=pygame.image.load('images/tecla_r.png')
    r = pygame.transform.scale(r, (50, 50))
    gameDisplay.blit(r,(display_width*0.45, display_height*0.81))
    esc = pygame.transform.scale(esc, (50, 50))
    gameDisplay.blit(esc,(display_width*0.55, display_height*0.81))
            

def parar_reiniciar():
    for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                if tecla=="escape":
                    return "Stop"
                elif tecla=="r":
                    return "Replay"

    
def game2(gameDisplay):
    
    pulsadas=[]
    descartadas=[]
    
    turno=piedra_papel_tijeras(gameDisplay)
    TURNOS.append(turno)
    
    pygame.display.set_caption('Aprendizaje Automático')
    clock = pygame.time.Clock()
    
    gameDisplay.fill(BLACK)
    logo=pygame.image.load('images/logo.png')
    logo = pygame.transform.scale(logo, (250, 57))
    gameDisplay.blit(logo,(10, 0))
    tablero = Tablero(8,8, FORMAS)
    board(tablero,gameDisplay)
    
    qtable = qlearning2(tablero.copy())

    out = False
    replay=False
    
    p1,p2=0,0
    print("COMIENZA EL JUEGO")
    
    while not out:
        
        i,_=tablero.siguiente_zero()
        p1, p2 = get_puntuacion(tablero)
        pygame.draw.rect(gameDisplay,BLACK,[0, display_height*0.85-60,display_width,100])
        display_text("P1:"+str(p1),display_width*0.2, display_height*0.85, 100, WHITE,gameDisplay)
        display_text("P2:"+str(p2),display_width*0.8, display_height*0.85, 100, WHITE,gameDisplay)
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                out = True
        if i!=-1:
            panel_letras(pulsadas,descartadas, gameDisplay)
            if TURNOS[-1]==1:
                print("Turno jugador 1")
                op=opciones(tablero)
                while not op:
#                     print("Descartamos la "+tablero.pentominos[0])
                    descartadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                ficha_colocada,replay,out=colocar_letra(tablero,op,gameDisplay)
                pulsadas.append(ficha_colocada.letra)
                TURNOS.append(2)
                pygame.display.update()
#                 print("Ficha: "+str(tablero.movimientos[-1][0]))
                print(tablero)
            else:
                print("Turno jugador 2")
                op=opciones(tablero)
                while not op:
                    print("Descartamos la "+tablero.pentominos[0])
                    descartadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                
                valida=False
                if not tablero.movimientos:
                    state=0
                else:
                    ultimo_movimiento=tablero.movimientos[-1][0]
                    state=tablero.fichas.index(ultimo_movimiento)
                
                rangos = rango_por_letra(FORMAS)
                action_completo = np.copy(qtable[state])#qtable[state] #Acciones para el estado
                print("Estado "+str(state))
                action_plano = np.squeeze(np.asarray(action_completo)) #Convertimos en array "aplaanamos"
                print("Rangos "+str(rangos))
                zona=rangos[tablero.pentominos[0]] #rango que nos indica las acciones siguientes permitidas
                print("Zona "+str(zona))
                action_cortado=action_plano[zona[0]:zona[1]+1] #cortamos el array para quedarnos solo con la zona de siguietes acciones #TODO revisar
                while not valida:
                    print("Zona "+str(action_cortado))
                    action_maximo = np.where(action_cortado==np.amax(action_cortado)) #cogemos los indices que tengan el valor maximo
                    print("Maximos "+str(action_maximo))
                    rand = random.randint(0,len(action_maximo[0])-1)
                    action_relativo = action_maximo[0][rand] #nos quedamos con el primero ya que todos serian iguales (se podria aleatorizar con epsilon)
                    action=posicion_real(action_relativo, tablero.pentominos[0], FORMAS) #obtenemos el indice real ya que le anterior era el indice ralivo al array cortado
                    action+=1
                    print("Ficha(numero) "+str(action))
                    pent = tablero.fichas[action-1]#Comprobar que entra, si no entra ponemos a -1000 esa posicion en la qtable y elegimos otro de los maximos
                    print("Ficha: "+str(pent))
                    pentomino=Pentomino(pent[0],int(pent[1]),int(pent[2]))
                    
                    x,y=tablero.comprobar_pentomino(pentomino)
                    
                    if x==-1:
                        print("No es valida")
                        action_cortado[action_relativo]=-1000
                    else:
                        print("Es valida")
                        valida=True
                tablero.colocar_pentomino_2p(pentomino, x, y, TURNOS[-1])
                teclas_escR(gameDisplay)
                pulsadas.append(pentomino.letra)
                tablero.buscar_huecos(TURNOS[-1])
                print(tablero)
                board(tablero,gameDisplay)
                TURNOS.append(1)
                pygame.display.update()
        elif i==-1:
            panel_letras(pulsadas,descartadas, gameDisplay)
            win(p1,p2,gameDisplay)
            teclas_escR(gameDisplay)
            pr=parar_reiniciar()
            if pr=="Replay":
                tablero=Tablero(8,8,FORMAS)
                pulsadas=[]
                board(tablero,gameDisplay)
                turno = random.randint(1,2)
                TURNOS.append(turno)
            elif pr=="Stop":
                out=True
        if replay:
            replay=False
            tablero=Tablero(8,8,FORMAS)
            pulsadas=[]
            board(tablero,gameDisplay)
            turno = random.randint(1,2)
            TURNOS.append(turno)
        pygame.display.update()
        
        clock.tick(30)
        
#     print(tablero)
#     print(tablero.movimientos)
    

def game3(gameDisplay):
    pulsadas=[]
    descartadas=[]
    
    turno=piedra_papel_tijeras(gameDisplay)
    TURNOS.append(turno)
    
    pygame.display.set_caption('Redes Neuronales')
    clock = pygame.time.Clock()
    
    gameDisplay.fill(BLACK)
    logo=pygame.image.load('images/logo.png')
    logo = pygame.transform.scale(logo, (250, 57))
    gameDisplay.blit(logo,(10, 0))
    tablero = Tablero(8,8, FORMAS)
    board(tablero, gameDisplay)
    
#     qtable = qlearning2(tablero.copy())
    red=red_neuronal()

    out = False
    replay=False
    
    p1,p2=0,0
    print("COMIENZA EL JUEGO")
    
    while not out:
        
        i,_=tablero.siguiente_zero()
        p1, p2 = get_puntuacion(tablero)
        pygame.draw.rect(gameDisplay,BLACK,[0, display_height*0.85-60,display_width,100])
        display_text("P1:"+str(p1),display_width*0.2, display_height*0.85, 100, WHITE, gameDisplay)
        display_text("P2:"+str(p2),display_width*0.8, display_height*0.85, 100, WHITE, gameDisplay)
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                out = True
        if i!=-1:
            panel_letras(pulsadas,descartadas, gameDisplay)
            if TURNOS[-1]==1:
                print("Turno jugador 1")
                op=opciones(tablero)
                while not op:
                    print("Descartamos la "+tablero.pentominos[0])
                    descartadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                    panel_letras(pulsadas,descartadas, gameDisplay)
                ficha_colocada,replay,out=colocar_letra(tablero,op, gameDisplay)
                
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
                    descartadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                    panel_letras(pulsadas,descartadas, gameDisplay)
                    print(tablero.pentominos)
                
                valida=False
                
                
                entrada=[] 
                aux=[0]*63
                if not tablero.movimientos:
                    estado=0
                    entrada.append(aux)
                    
                else:
                    ultimo_movimiento=tablero.movimientos[-1][0]
                    estado=tablero.fichas.index(ultimo_movimiento)
                    print(estado)
                    aux[estado]=1
                    entrada.append(aux)
                print(entrada)
                solucion=red.sim(entrada)
                
                old_action=-1
                while not valida:
                    action=get_max(tablero.pentominos[0],solucion[0])
    #                 action+=1
                    print("Estado, accion: ("+str(estado)+", "+str(action)+")")
                    
                    pent = tablero.fichas[action]#Comprobar que entra, si no entra, elegimos otro de los m�ximos
                    print("Ficha: "+str(pent))
                    pentomino=Pentomino(pent[0],int(pent[1]),int(pent[2]))
                    
                    x,y=tablero.comprobar_pentomino(pentomino)
                        
                    if x==-1:
                        print("No es valida")
                        print("(Acation, OldAction) ("+str(action)+", "+str(old_action)+")")
                        if old_action==action:
                            descartadas.append(tablero.pentominos[0])
                            tablero.pentominos.pop(0)
#                                 op=opciones(tablero)
                            panel_letras(pulsadas,descartadas,gameDisplay)
                        else:
                            solucion[0][action+1]=0
                            old_action=action
                    else:
                        print("Es valida")
                        valida=True
                            
                tablero.colocar_pentomino_2p(pentomino, x, y, TURNOS[-1])
                teclas_escR(gameDisplay)
                pulsadas.append(pentomino.letra)
                tablero.buscar_huecos(TURNOS[-1])
                print(tablero)
                board(tablero, gameDisplay)
                TURNOS.append(1)
                pygame.display.update()
        elif i==-1:
            panel_letras(pulsadas,descartadas, gameDisplay)
            win(p1,p2, gameDisplay)
            teclas_escR(gameDisplay)
            pr=parar_reiniciar()
            if pr=="Replay":
                tablero=Tablero(8,8,FORMAS)
                pulsadas=[]
                board(tablero, gameDisplay)
                turno = random.randint(1,2)
                TURNOS.append(turno)
            elif pr=="Stop":
                out=True
        if replay:
            replay=False
            tablero=Tablero(8,8,FORMAS)
            pulsadas=[]
            board(tablero, gameDisplay)
            turno = random.randint(1,2)
            TURNOS.append(turno)
        pygame.display.update()
        
        clock.tick(30)
        
#     print(tablero)
#     print(tablero.movimientos)


def game4(gameDisplay):
    pulsadas=[]
    descartadas=[]
    
#     turno = random.randint(1,2)
#     TURNOS.append(random.randint(1,2))
    
    pygame.display.set_caption('Dos Jugadores')
    clock = pygame.time.Clock()
    gameDisplay.fill(BLACK)
    
    logo=pygame.image.load('images/logo.png')
    logo = pygame.transform.scale(logo, (250, 57))
    gameDisplay.blit(logo,(10, 0))
    
    display_text("¿Quien juega primero?",display_width*0.50, display_height*0.15, 50, WHITE,gameDisplay)
    display_text("Jugador 1",display_width*0.25, display_height*0.65, 60, ROJO,gameDisplay)
    display_text("Jugador 2",display_width*0.75, display_height*0.65, 60, AZUL,gameDisplay)
    display_text("VS.",display_width*0.50, display_height*0.60, 100, WHITE,gameDisplay)
    tecla_1=pygame.image.load('images/tecla_1.png')
    tecla_1 = pygame.transform.scale(tecla_1, (100, 100))
    gameDisplay.blit(tecla_1,(display_width*0.21, display_height*0.48))
    tecla_2=pygame.image.load('images/tecla_2.png')
    tecla_2 = pygame.transform.scale(tecla_2, (100,100))
    gameDisplay.blit(tecla_2,(display_width*0.71, display_height*0.48))
    
    pygame.display.update()
    turno=0
    out=False
    while not out:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                if tecla == "1":
                    turno=1
                    out=True
                elif tecla=="2":
                    turno=2
                    out=True
                    
    TURNOS.append(turno)
    
    gameDisplay.fill(BLACK)
    gameDisplay.blit(logo,(10, 0))
    tablero = Tablero(8,8, FORMAS)
    board(tablero, gameDisplay)
    
    out = False
    replay=False
    
    p1,p2=0,0
    print("COMIENZA EL JUEGO")
    
    while not out:
        
        i,_=tablero.siguiente_zero()
        p1, p2 = get_puntuacion(tablero)
        pygame.draw.rect(gameDisplay,BLACK,[0, display_height*0.85-60,display_width,100])
        display_text("P1:"+str(p1),display_width*0.2, display_height*0.85, 100, WHITE, gameDisplay)
        display_text("P2:"+str(p2),display_width*0.8, display_height*0.85, 100, WHITE, gameDisplay)
        
        if i!=-1:
            panel_letras(pulsadas,descartadas, gameDisplay)
            if TURNOS[-1]==1:
                print("Turno jugador 1")
                op=opciones(tablero)
                while not op:
                    print("Descartamos la "+tablero.pentominos[0])
                    descartadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                    panel_letras(pulsadas,descartadas, gameDisplay)
                ficha_colocada,replay,out=colocar_letra(tablero,op, gameDisplay)
                
                pulsadas.append(ficha_colocada.letra)
                TURNOS.append(2)
                pygame.display.update()
#                 print("Ficha: "+str(tablero.movimientos[-1][0]))
                print(tablero)
            else:
                print("Turno jugador 2")
                op=opciones(tablero)
                while not op:
                    print("Descartamos la "+tablero.pentominos[0])
                    descartadas.append(tablero.pentominos[0])
                    tablero.pentominos.pop(0)
                    op=opciones(tablero)
                    panel_letras(pulsadas,descartadas, gameDisplay)
                ficha_colocada,replay,out=colocar_letra(tablero,op, gameDisplay)
                
                pulsadas.append(ficha_colocada.letra)
                TURNOS.append(1)
                pygame.display.update()
#                 print("Ficha: "+str(tablero.movimientos[-1][0]))
                print(tablero)
        elif i==-1:
            panel_letras(pulsadas,descartadas, gameDisplay)
            win(p1,p2, gameDisplay)
            teclas_escR(gameDisplay)
            pr=parar_reiniciar()
            if pr=="Replay":
                tablero=Tablero(8,8,FORMAS)
                pulsadas=[]
                board(tablero, gameDisplay)
                turno = random.randint(1,2)
                TURNOS.append(turno)
            elif pr=="Stop":
                out=True
        if replay:
            replay=False
            tablero=Tablero(8,8,FORMAS)
            pulsadas=[]
            board(tablero, gameDisplay)
            turno = random.randint(1,2)
            TURNOS.append(turno)
        pygame.display.update()
        
        clock.tick(30)


def piedra_papel_tijeras(gameDisplay):
    gameDisplay.fill(BLACK)
    logo=pygame.image.load('images/logo.png')
    logo = pygame.transform.scale(logo, (250, 57))
    gameDisplay.blit(logo,(10, 0))
    
    display_text("¿Quien juega primero?",display_width*0.50, display_height*0.05, 50, WHITE,gameDisplay)
    display_text("Piedra, Pepel o Tijeras",display_width*0.50, display_height*0.15, 60, WHITE,gameDisplay)
    
    piedra=pygame.image.load('images/piedra.png')
    papel=pygame.image.load('images/papel.png')
    tijeras=pygame.image.load('images/tijeras.png')
    piedra_hover=pygame.image.load('images/piedra_hover.png')
    papel_hover=pygame.image.load('images/papel_hover.png')
    tijeras_hover=pygame.image.load('images/tijeras_hover.png')
    
    piedra = pygame.transform.scale(piedra, (250, 250))
    papel = pygame.transform.scale(papel, (250, 250))
    tijeras = pygame.transform.scale(tijeras, (250, 250))
    piedra_hover = pygame.transform.scale(piedra_hover, (250, 250))
    papel_hover = pygame.transform.scale(papel_hover, (250, 250))
    tijeras_hover = pygame.transform.scale(tijeras_hover, (250, 250))
    
    corona=pygame.image.load('images/corona.png')
    corona = pygame.transform.scale(corona, (70, 70))
    
    ppt={1:piedra,2:papel,3:tijeras}
    
    pygame.display.update()
    
    out=False
    eleccion=1
    turno=0
    gameDisplay.blit(piedra_hover,(display_width*0.40, display_height*0.21))
    gameDisplay.blit(papel,(display_width*0.25, display_height*0.61))
    gameDisplay.blit(tijeras,(display_width*0.55, display_height*0.61))   
    while not out:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                if tecla == "a":
                    eleccion=2
                    gameDisplay.blit(piedra,(display_width*0.40, display_height*0.21))
                    gameDisplay.blit(papel_hover,(display_width*0.25, display_height*0.61))
                    gameDisplay.blit(tijeras,(display_width*0.55, display_height*0.61)) 
                    pygame.display.update()
                if  tecla == "d":
                    eleccion=3
                    gameDisplay.blit(piedra,(display_width*0.40, display_height*0.21))
                    gameDisplay.blit(papel,(display_width*0.25, display_height*0.61))
                    gameDisplay.blit(tijeras_hover,(display_width*0.55, display_height*0.61)) 
                    pygame.display.update()
                if  tecla == "w":
                    eleccion=1
                    gameDisplay.blit(piedra_hover,(display_width*0.40, display_height*0.21))
                    gameDisplay.blit(papel,(display_width*0.25, display_height*0.61))
                    gameDisplay.blit(tijeras,(display_width*0.55, display_height*0.61))   
                    pygame.display.update()
                if tecla == "return":
                    out=True
                    

    out=False
    while not out:      
        if turno==0:
            p2 = random.randint(1,3)
            if p2==eleccion:
                turno=random.randint(1,2)
            elif eleccion==1 and p2==3 or eleccion==3 and p2==2 or eleccion==2 and p2==1:
                turno=1
            else:
                turno=2
                
            gameDisplay.fill(BLACK)
            gameDisplay.blit(logo,(10, 0))
            display_text("Resultado",display_width*0.50, display_height*0.15, 60, WHITE,gameDisplay)
            display_text("Pulsa cualquier tecla para comenzar el juego",display_width*0.50, display_height*0.95, 30, WHITE,gameDisplay)
            print(ppt)
            gameDisplay.blit(ppt[eleccion],(display_width*0.25, display_height*0.31))
            gameDisplay.blit(ppt[p2],(display_width*0.55, display_height*0.31))
            if turno==1:
                display_text("Comienza el jugador 1",display_width*0.50, display_height*0.85, 40, WHITE,gameDisplay)
                xy=(display_width*0.25, display_height*0.30)
            else:
                display_text("Comienza el jugador 2",display_width*0.50, display_height*0.85, 40, WHITE,gameDisplay)
                xy=(display_width*0.55, display_height*0.30)
            gameDisplay.blit(corona,xy)
            
            if eleccion==p2:
                display_text("Empate, el jugador ha sido elegido de forma aleatoria",display_width*0.50, display_height*0.75, 20, WHITE,gameDisplay)
            
                
            pygame.display.update()
            
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                out=True
    
    
    
    gameDisplay.fill(BLACK)
    return turno
                   

def inicio():
    pygame.init()
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Menu Principal')
    icon_surf = pygame.image.load('images/tetris.ico')
    pygame.display.set_icon(icon_surf)
    
    gameDisplay.fill(BLACK)
    
    logo=pygame.image.load('images/logo.png')
    gameDisplay.blit(logo,(30,40))
    
    display_text("Redes Neuronales",display_width*0.27, display_height*0.76, 35, WHITE,gameDisplay)
    display_text("Aprendizaje Automático",display_width*0.30, display_height*0.56, 35, WHITE,gameDisplay)
    display_text("Dos Jugadores",display_width*0.70, display_height*0.65, 35, WHITE,gameDisplay)
    tecla_a=pygame.image.load('images/tecla_a.png')
    tecla_r=pygame.image.load('images/tecla_r.png')
    tecla_q=pygame.image.load('images/tecla_q.png')
    tecla_r = pygame.transform.scale(tecla_r, (80, 80))
    gameDisplay.blit(tecla_r,(display_width*0.10, display_height*0.70))
    tecla_a = pygame.transform.scale(tecla_a, (80, 80))
    gameDisplay.blit(tecla_a,(display_width*0.10, display_height*0.50))
    tecla_q = pygame.transform.scale(tecla_q, (80, 80))
    gameDisplay.blit(tecla_q,(display_width*0.55, display_height*0.59))
    
    display_text("Salir",display_width*0.87, display_height*0.90, 25, WHITE,gameDisplay)
    esc=pygame.image.load('images/tecla_esc.png')
    esc = pygame.transform.scale(esc, (50, 50))
    gameDisplay.blit(esc,(display_width*0.85, display_height*0.81))
    
    pygame.display.update()
    
    return gameDisplay
    

if __name__=="__main__":
    
    gameDisplay=inicio()
    
    out=False
    while not out:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                if tecla == "r":
                    game3(gameDisplay)
                    gameDisplay=inicio()
                elif tecla== "a":
                    game2(gameDisplay)
                    gameDisplay=inicio()
                elif tecla== "q":
                    game4(gameDisplay)
                    gameDisplay=inicio()
                elif tecla=="escape":
                    out=True
            if event.type is pygame.QUIT:
                out=True
    
    pygame.quit()
    quit()
    
#     game3(gameDisplay)