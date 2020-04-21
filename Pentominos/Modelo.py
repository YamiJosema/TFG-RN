import numpy as np
from Pentominos.Formas import modelo
from Pentominos.Utilidades import cargar_pentominos, Formas
import random 


class Tablero:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.done = False;
        self.board = np.zeros((x,y), dtype=np.int)
        self.pentominos=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
        self.movimientos=[]
        self.fichas_colocadas=0
        self.fichas=cargar_pentominos()
        self.piezas=[]
        
    
    def copy(self):
        tablero=Tablero(self.x,self.y)
        tablero.done = self.done;
        tablero.board = np.copy(self.board)
        aux=[]
        aux.append(self.pentominos)
        tablero.pentominos=aux
        aux=[]
        aux.append(self.movimientos)
        tablero.movimientos=aux
        tablero.fichas_colocadas=self.fichas_colocadas
        aux=[]
        aux.append(self.piezas)
        tablero.piezas=aux
        
        return tablero


    def reset(self):
        self.done = False;
        self.board = np.zeros((self.x,self.y), dtype=np.int)
        self.pentominos=["F","I","L","N","P","T","U","V","W","X","Y","Z"]
        self.movimientos=[]
        self.fichas_colocadas=0
        self.piezas=[]
        return 0,0,False
    
    
    def ficha_aleatoria(self):
#         print("Ficha aleatoria")
        no_inversa=["T","U","V","W"]
        letra=self.pentominos[0]
        if letra in no_inversa:
            rotacion=str(random.randint(0,3))
            inversa="0"
        elif letra=="Z":
            rotacion=str(random.randint(0,1))
            inversa=str(random.randint(0,1))
        elif letra=="X":
            rotacion="0"
            inversa="0"
        elif letra=="I":
            rotacion=str(random.randint(0,1))
            inversa="0"
        else:
            rotacion=str(random.randint(0,3))
            inversa=str(random.randint(0,1))
        ficha=[letra, rotacion, inversa]
        action = self.fichas.index(ficha)
        
        return action
    

    def colocar_siguiente(self, action,state):
#         print("Colocar siguiente")
        penalizacion=0
        pent=self.fichas[action]
        pentomino = Pentomino(pent[0],int(pent[1]),int(pent[2]))
        if pentomino.letra in self.pentominos:
            colocado=False
            for i in range(0,self.x):
                for j in range(0,self.y):
#                     if self.board[i][j]==0:
                    colocado=self.colocar_sin_superposicion(pentomino, i,j)
#                         print("Intentamos colocar la ficha "+str(action)+" en la posicion ("+str(i)+", "+str(j)+")")
                    if colocado:break
                if colocado:break
            if colocado:
#                 print("Colocada satisfactoriamente en la posicion ("+str(i)+", "+str(j)+")")
                self.fichas_colocadas+=1
                
#                 ficha=[pentomino.letra,str(pentomino.rotacion),str(pentomino.invertido)]
                next_state=action
                
                self.buscar_huecos(action)
                penalizacion=self.penalizacion(action)
#                 penalizacion*=0.1#0.2
                
                self.piezas.append(action)
            else:
#                 print("La ficha no puede ser colocada en el tablero")
#                TODO penalizar en puntos si la ficha no se puede colocar en el tablero (interesante que el tablero guarde las puntiaciones)
                next_state=state
        else:
            next_state=state
        
        reward=penalizacion*-10 if next_state!=state else -1000 #TODO penalizacion por huecos
        
        fin,_=self.siguiente_zero()
        done=True if fin==-1 else False

        return next_state, reward, done 
    
    
    def colocar_sin_superposicion(self, pentomino, x, y):
#         print("Colocar sin superposicion")
        aux_board = np.copy(self.board)
        resultado= self.colocar_pentomino(pentomino, x, y)
        if resultado:
            ind = np.unravel_index(np.argmax(self.board, axis=None), self.board.shape)  
            if self.board[ind]!=1:
                self.board=aux_board
                return False
            else:
                self.pentominos.remove(pentomino.letra)
        return resultado
    
    
    def comprobar_pentomino_individual(self, pentomino, x, y):
        if x>=0 and y>=0:
            for i in range(len(pentomino.modelo)):
                for j in range(len(pentomino.modelo[0])):
                    if x+i<self.x and y+j<self.y:
                        if pentomino.modelo[i][j]==1 and self.board[x+i][y+j]!=0:
                            return False
                    else:
                        return False
            return True
        else:
            return False
    
    
    def comprobar_pentomino(self, pentomino):
        valido=False
        while not valido:
            pos_x, pos_y=self.siguiente_zero()
            if pos_x==-1:
                break
            if pentomino.letra=="X" or (pentomino.letra=="T" and pentomino.modelo[0][0]==0):
                org_y=pos_y-1
#                 print("LETRA X: "+pentomino.letra)
#                 print("Origniales: ("+str(pos_x)+", "+str(org_y)+")")
                valido=self.comprobar_pentomino_individual(pentomino,pos_x,org_y)
#                 print("Valido O: "+str(valido))
                if valido:
                    pos_y=org_y
                if not valido and org_y>=0:
                    self.board[pos_x][pos_y]=10
            if not valido:
#                 print("LETRA: "+pentomino.letra)
#                 print("Origniales: ("+str(pos_x)+", "+str(pos_y)+")")
                valido_O=self.comprobar_pentomino_individual(pentomino,pos_x,pos_y)
#                 print("Valido O: "+str(valido_O))
                aux_y=pos_y-(len(pentomino.modelo[0])-1)
#                 print("Modificados: ("+str(pos_x)+", "+str(aux_y)+")")
                valido_M=self.comprobar_pentomino_individual(pentomino,pos_x, aux_y)
#                 print("Valido M: "+str(valido_M))
                if valido_M:
                    pos_y=aux_y
                if not valido_O and not valido_M:
                    self.board[pos_x][pos_y]=10
                valido=valido_O  or valido_M
        self.limpiar_huecos()
#         print("Posicion Final: ("+str(pos_x)+", "+str(pos_y)+")")
        return pos_x, pos_y
    
    
    def siguiente_zero(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]==0:
                    return i,j
        i=-1
        j=-1
        return i, j
    
    
    def penalizacion(self,action):
#         print("Penalizacion")
        if action==0:
            action=100
        count=0
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j]==action*-1:
                    count+=1
        return count
    
    
    def buscar_huecos(self, jugador):
#         print("Buscar huecos")
#         self.huecos_individuales(jugador)
        self.huecos_menores(jugador)
        self.limpiar_huecos()
    
    
    def huecos_individuales(self, jugador):
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j]==0:
                    if i==0 and j==0:
                        if self.board[i][j+1]!=0 and self.board[i+1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif i==self.x-1 and j==self.y-1:
                        if self.board[i][j-1]!=0 and self.board[i-1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif i==0 and j==self.y-1:
                        if self.board[i][j-1]!=0 and self.board[i+1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif j==0 and i==self.x-1:
                        if self.board[i][j+1]!=0 and self.board[i-1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif i==0:
                        if self.board[i][j-1]!=0 and self.board[i][j+1]!=0 and self.board[i+1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif j==0:
                        if self.board[i][j+1]!=0 and self.board[i-1][j]!=0 and self.board[i+1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif i==self.x-1:
                        if self.board[i][j-1]!=0 and self.board[i][j+1]!=0 and self.board[i-1][j]!=0:
                            self.board[i][j]=jugador*-1
                    elif j==self.y-1:
                        if self.board[i][j-1]!=0 and self.board[i-1][j]!=0 and self.board[i+1][j]!=0:
                            self.board[i][j]=jugador*-1
                    else:
                        if self.board[i][j-1]!=0 and self.board[i][j+1]!=0 and self.board[i-1][j]!=0 and self.board[i+1][j]!=0:
                            self.board[i][j]=jugador*-1
                            
                            
    def limpiar_huecos(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j]==10:
                    self.board[i][j]=0   
    
    
# --------------------------------------------------OTROS METODOS-------------------------------------------------------------------    
    def todos_usados(self):
        if not self.pentominos:
            self.done=True
            return True
        else:
            self.done=False
            return False
        
    
    def colocar_pentomino(self, pentomino, x, y):
#         print("Colocar pentomino")
        row=len(pentomino.modelo)
        cols=len(pentomino.modelo[0])
        if x<self.x and y<self.y and row<=self.x-x and cols<=self.y-y:
            cx = x
            cy = y
            for i in range(row):
                for j in range(cols):
                    self.board[cx][cy]+=pentomino.modelo[i][j]
                    cy+=1
                cx+=1
                cy=y
            return True
        return False
    
    
    def colocar_pentomino_2p(self, pentomino, x, y, jugador):
#         print("Colocar pentomino 2p")
        colocado=True
        row=len(pentomino.modelo)
        cols=len(pentomino.modelo[0])
        aux_board = np.copy(self.board)
        if x<self.x and y<self.y and row<=self.x-x and cols<=self.y-y and x>=0 and y>=0 and x<self.x and y<self.y:
            cx = x
            cy = y
            for i in range(row):
                for j in range(cols):
                    if pentomino.modelo[i][j]==1:
                        if self.board[cx][cy]!=0:
                            self.board=aux_board
                            colocado=False
                        else:
                            self.board[cx][cy]=jugador
                    if not colocado:
                        break
                    cy+=1
                if not colocado:
                    break
                cx+=1
                cy=y
            if colocado:
                self.pentominos.remove(pentomino.letra)
                self.movimientos.append((pentomino,x,y))
                self.fichas_colocadas+=1
        else:
            colocado=False
        return colocado
    
    
    def uno_cerca(self, i,j):
        cerca=False
        if i==0 or j==0 or i==self.x-1 or j==self.y-1:
            cerca=True
        elif self.board[i][j-1]!=0 or self.board[i][j+1]!=0 or self.board[i-1][j]!=0 or self.board[i+1][j]!=0:
            cerca=True
        return cerca
    
    
    def cerrar_hueco(self,huecos):
        for h in huecos:
            self.board[h[0]][h[1]]=10
                
    
    def comprobar_fichas(self,i,j,aux_board): #Done
#         print("Comprobar fichas")
        tablero_aux=Tablero(len(aux_board),len(aux_board[0]))
        tablero_aux.board=np.copy(aux_board)
        for letra in self.pentominos:
            for rot in range(4):
                for inv in range(2):
                    pent=Pentomino(letra,rot,inv)
#                     print("Letra: "+letra)
#                     print("Rotacion: "+str(rot))
#                     print("Inversion: "+str(inv))
#                     print("Posicion: "+str(i)+" "+str(j))
                    colocado=tablero_aux.colocar_pentomino_2p(pent, i, j,1)
                    posicion = (i,j) if colocado else (-1,-1)
                    if not colocado:
#                         print("Posicion: "+str(i-(len(pent.modelo)-1))+" "+str(j))
                        colocado=tablero_aux.colocar_pentomino_2p(pent, i-(len(pent.modelo)-1), j,1)
                        posicion = (i-(len(pent.modelo)-1), j) if colocado else (-1,-1)
                    if not colocado:
#                         print("Posicion: "+str(i-(len(pent.modelo)-1))+" "+str(j-(len(pent.modelo[0])-1)))
                        colocado=tablero_aux.colocar_pentomino_2p(pent, i-(len(pent.modelo)-1), j-(len(pent.modelo[0])-1),1)
                        posicion = (i-(len(pent.modelo)-1), j-(len(pent.modelo[0])-1)) if colocado else (-1,-1)
                    if not colocado:
#                         print("Posicion: "+str(i)+" "+str(j-(len(pent.modelo[0])-1)))
                        colocado=tablero_aux.colocar_pentomino_2p(pent, i, j-(len(pent.modelo[0])-1),1)
                        posicion = (i, j-(len(pent.modelo[0])-1)) if colocado else (-1,-1)
                    if colocado:
#                         print(tablero_aux)
                        return True, posicion[0], posicion[1]
        return False,-1,-1


    def hueco_real(self,aux_board, huecos): #Done
#         print("Hueco real")
        real=False
        for h in huecos:
#             print("Recorriendo hueco "+str(h))
            real=self.comprobar_fichas(h[0], h[1], aux_board)[0]
            if real:
                break
        return real
            
    
    def huecos_menores_busqueda(self, i, j, jugador): #Done
        if jugador==0:
            jugador=100
#         print("huecos menores busqueda")
        huecos=[]
        huecos.append((i,j))
        for h in huecos:
#             print(len(h))
            if h[0]<self.x-1 and self.board[h[0]+1][h[1]]==0 and self.uno_cerca(h[0]+1,h[1]):
                huecos.append((h[0]+1,h[1]))
                self.board[h[0]+1][h[1]]=jugador*-1
            if h[1]<self.y-1 and self.board[h[0]][h[1]+1]==0 and self.uno_cerca(h[0],h[1]+1):
                huecos.append((h[0],h[1]+1))
                self.board[h[0]][h[1]+1]=jugador*-1
            if h[0]>0 and self.board[h[0]-1][h[1]]==0 and self.uno_cerca(h[0]-1,h[1]):
                huecos.append((h[0]-1,h[1]))
                self.board[h[0]-1][h[1]]=jugador*-1
            if h[1]>0 and self.board[h[0]][h[1]-1]==0 and self.uno_cerca(h[0],h[1]-1):
                huecos.append((h[0],h[1]-1))
                self.board[h[0]][h[1]-1]=jugador*-1
                
#             print("----------------------------")    
#             print(self.board)
#             print(huecos)
#             print("----------------------------")   
#         print("Salimos!")
        return huecos
                
    
    def huecos_menores(self, jugador): #DONE
#         print("Huecos menores")
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j]==0 and self.uno_cerca(i, j):
                    hueco=True
                    aux_board = np.copy(self.board)
                    self.board[i][j]=jugador*-1
                    huecos=self.huecos_menores_busqueda(i,j, jugador)
                    count=len(huecos)
#                     print("Total:"+str(count))
#                     print(huecos)
                    if count>=5:
                        if count<=12:
#                             print(huecos)
#                             print("Entrando en hueco_real en "+str(i)+","+str(j))
                            hueco=self.hueco_real(aux_board, huecos)
#                             print("Es un hueco real?:"+str(hueco))
                        if hueco:
                            self.board=aux_board
                            self.cerrar_hueco(huecos)
                            
                            
    def __str__(self):
        return str(self.board)
    def __unicode__(self):
        return str(self.board)
    def __repr__(self):
        return str(self.board)
    def __getitem__(self):
        return self.board


class Pentomino:
    def __init__(self, letra, rotacion=0, invertido=0): #Rotacion a 0 e invertido en false por defecto
        #Comprobar que la letra es correcta TODO
        self.letra=letra
        self.modelo=modelo(letra) #F I L N P T U V W X Y Z
        self.invertido=invertido
        self.rotacion=rotacion
        if letra!="I" and letra!="X" and invertido:
            self.invertir()
        if letra!="X" and rotacion!=0:
            self.rotar(rotacion)
    
    def rotar(self,rotacion):
        while rotacion>0:
            size=len(self.modelo[0])
            if size==1:
                self.modelo=np.array([[1,1,1,1,1]])
            else:
                c1 = np.copy(self.modelo[:,0])
                c2 = np.copy(self.modelo[:,1])
                if size==2:
                    self.modelo=np.vstack((c2,c1))
                elif size==3:
                    c3 = np.copy(self.modelo[:,2])
                    self.modelo=np.vstack((c3,c2,c1))
                elif size==4:
                    c3 = np.copy(self.modelo[:,2])
                    c4 = np.copy(self.modelo[:,3])
                    self.modelo=np.vstack((c4,c3,c2,c1))
                elif size==5:
                    c3 = np.copy(self.modelo[:,2])
                    c4 = np.copy(self.modelo[:,3])
                    c5 = np.copy(self.modelo[:,4])
                    self.modelo=np.vstack((c5,c4,c3,c2,c1))
            rotacion-=1
    
    def invertir(self):
        if self.letra!='I' and self.letra!='X':
            longitud = len(self.modelo[0])
            c1 = np.copy(self.modelo[:,0])
            if longitud==2:
                c2 = np.copy(self.modelo[:,1])
                self.modelo[:,0]=c2
                self.modelo[:,1]=c1
            elif longitud==3:
                c3 = np.copy(self.modelo[:,2])
                self.modelo[:,0]=c3
                self.modelo[:,2]=c1 
            elif longitud==4:
                c2 = np.copy(self.modelo[:,1])
                c3 = np.copy(self.modelo[:,2])
                c4 = np.copy(self.modelo[:,3])
                self.modelo[:,0]=c4
                self.modelo[:,1]=c3
                self.modelo[:,2]=c2
                self.modelo[:,3]=c1
    
    def __str__(self):
        return str(self.modelo)
    def __unicode__(self):
        return str(self.modelo)
    def __repr__(self):
        return str(self.modelo)
    def __getitem__(self):
        return self.modelo
    

class Estado:
    def __init__(self,tablero,padre):
        self.tablero=tablero
        self.descartado = False
        self.padre=padre
        self.movimientos=[]
        
    def avanzar(self,pentomino,x,y):
        estado = Estado(self.tablero,self)
        estado.tablero.colocar_sin_superposicion(pentomino,x,y)
        estado.movimientos.append(pentomino)
        return estado
    
    def __str__(self):
        return str(self.tablero)
    def __unicode__(self):
        return str(self.tablero)
    def __repr__(self):
        return str(self.tablero)
    def __getitem__(self):
        return self.tablero
        
            
    