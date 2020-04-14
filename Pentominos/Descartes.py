'''
Created on 2 abr. 2019

@author: Josema
'''
# def busqueda_profunidad():
#     tablero = Tablero(8,8)
#     actual = Estado(tablero, None)
#     estados = []
#     estados.append(actual)
#     while not tablero.todos_usados():
#         contador=len(tablero.pentominos)
#         letras=[]
#         letras.extend(tablero.pentominos)
#         while contador>0:
#             size=len(actual.tablero.pentominos)
#             letra=actual.tablero.pentominos[random.randint(0,size-1)]
#             #Probar con todas las posturas de la forma
#             pentomino = Pentomino(letra,random.randint(0,3),random.randint(0,1))
#             x,y=tablero.siguiente_zero()
#             print str(x)+"-"+str(y)
#             nuevo_estado=actual.avanzar(pentomino,x,y)
#             estados.append(nuevo_estado)
#             actual=nuevo_estado
#         print actual


#Antiguo metodo para construir la entrada y el objetivo
#     with open('csv/entrenamiento.csv', 'rb') as f:
#         reader = csv.reader(f)
# 
#         arr = []
#         for row in reader:
#             arr['tablero']=row[0]
#             arr['ficha']=row[1]
        
#         pent_entrenamiento, pent_prueba = cross_validation.train_test_split(arr, test_size=.33, random_state=2346523,stratify=arr[1])
#         print pent_entrenamiento
#         print pent_prueba
#         for row in reader:
#             ent=row[0].replace("[", "")
#             ent2=ent.replace("]", "")
#             entradaR= map(int,ent2.split())
#             for i in range(len(entradaR),fichas):
#                 entradaR.append(0)
#             entrada.append(entradaR)
#             obj=int(row[1])
#             obj_array= [0]*63
#             obj_array[obj]=1
#             objetivo.append(obj_array)


# --------------------------------------------------MODELO-------------------------------------------------------------------    
#     def todos_usados(self):
#         if not self.pentominos:
#             self.done=True
#             return True
#         else:
#             self.done=False
#             return False
#         
#     
#     def colocar_pentomino(self, pentomino, x, y):
# #         print("Colocar pentomino")
#         row=len(pentomino.modelo)
#         cols=len(pentomino.modelo[0])
#         if x<self.x and y<self.y and row<=self.x-x and cols<=self.y-y:
#             cx = x
#             cy = y
#             for i in range(row):
#                 for j in range(cols):
#                     self.board[cx][cy]+=pentomino.modelo[i][j]
#                     cy+=1
#                 cx+=1
#                 cy=y
#             return True
#         return False
#     
#     
#     def colocar_pentomino_2p(self, pentomino, x, y, jugador):
# #         print("Colocar pentomino 2p")
#         colocado=True
#         row=len(pentomino.modelo)
#         cols=len(pentomino.modelo[0])
#         aux_board = np.copy(self.board)
#         if x<self.x and y<self.y and row<=self.x-x and cols<=self.y-y and x>=0 and y>=0 and x<self.x and y<self.y:
#             cx = x
#             cy = y
#             for i in range(row):
#                 for j in range(cols):
#                     if pentomino.modelo[i][j]==1:
#                         if self.board[cx][cy]!=0:
#                             self.board=aux_board
#                             colocado=False
#                         else:
#                             self.board[cx][cy]=jugador
#                     if not colocado:
#                         break
#                     cy+=1
#                 if not colocado:
#                     break
#                 cx+=1
#                 cy=y
#             if colocado:
#                 self.pentominos.remove(pentomino.letra)
#                 self.movimientos.append((pentomino,x,y))
#                 self.fichas_colocadas+=1
#         else:
#             colocado=False
#         return colocado
#     
#     
#     def uno_cerca(self, i,j):
#         cerca=False
#         if i==0 or j==0 or i==self.x-1 or j==self.y-1:
#             cerca=True
#         elif self.board[i][j-1]!=0 or self.board[i][j+1]!=0 or self.board[i-1][j]!=0 or self.board[i+1][j]!=0:
#             cerca=True
#         return cerca
#     
#     
#     def cerrar_hueco(self,huecos):
#         for h in huecos:
#             self.board[h[0]][h[1]]=10
#                 
#     
#     def comprobar_fichas(self,i,j,aux_board): #Done
# #         print("Comprobar fichas")
#         tablero_aux=Tablero(len(aux_board),len(aux_board[0]))
#         tablero_aux.board=np.copy(aux_board)
#         for letra in self.pentominos:
#             for rot in range(4):
#                 for inv in range(2):
#                     pent=Pentomino(letra,rot,inv)
# #                     print("Letra: "+letra)
# #                     print("Rotacion: "+str(rot))
# #                     print("Inversion: "+str(inv))
# #                     print("Posicion: "+str(i)+" "+str(j))
#                     colocado=tablero_aux.colocar_pentomino_2p(pent, i, j,1)
#                     posicion = (i,j) if colocado else (-1,-1)
#                     if not colocado:
# #                         print("Posicion: "+str(i-(len(pent.modelo)-1))+" "+str(j))
#                         colocado=tablero_aux.colocar_pentomino_2p(pent, i-(len(pent.modelo)-1), j,1)
#                         posicion = (i-(len(pent.modelo)-1), j) if colocado else (-1,-1)
#                     if not colocado:
# #                         print("Posicion: "+str(i-(len(pent.modelo)-1))+" "+str(j-(len(pent.modelo[0])-1)))
#                         colocado=tablero_aux.colocar_pentomino_2p(pent, i-(len(pent.modelo)-1), j-(len(pent.modelo[0])-1),1)
#                         posicion = (i-(len(pent.modelo)-1), j-(len(pent.modelo[0])-1)) if colocado else (-1,-1)
#                     if not colocado:
# #                         print("Posicion: "+str(i)+" "+str(j-(len(pent.modelo[0])-1)))
#                         colocado=tablero_aux.colocar_pentomino_2p(pent, i, j-(len(pent.modelo[0])-1),1)
#                         posicion = (i, j-(len(pent.modelo[0])-1)) if colocado else (-1,-1)
#                     if colocado:
# #                         print(tablero_aux)
#                         return True, posicion[0], posicion[1]
#         return False,-1,-1
# 
# 
#     def hueco_real(self,aux_board, huecos): #Done
# #         print("Hueco real")
#         real=False
#         for h in huecos:
# #             print("Recorriendo hueco "+str(h))
#             real=self.comprobar_fichas(h[0], h[1], aux_board)[0]
#             if real:
#                 break
#         return real
#             
#     
#     def huecos_menores_busqueda(self, i, j, jugador): #Done
#         if jugador==0:
#             jugador=100
# #         print("huecos menores busqueda")
#         huecos=[]
#         huecos.append((i,j))
#         for h in huecos:
# #             print(len(h))
#             if h[0]<self.x-1 and self.board[h[0]+1][h[1]]==0 and self.uno_cerca(h[0]+1,h[1]):
#                 huecos.append((h[0]+1,h[1]))
#                 self.board[h[0]+1][h[1]]=jugador*-1
#             if h[1]<self.y-1 and self.board[h[0]][h[1]+1]==0 and self.uno_cerca(h[0],h[1]+1):
#                 huecos.append((h[0],h[1]+1))
#                 self.board[h[0]][h[1]+1]=jugador*-1
#             if h[0]>0 and self.board[h[0]-1][h[1]]==0 and self.uno_cerca(h[0]-1,h[1]):
#                 huecos.append((h[0]-1,h[1]))
#                 self.board[h[0]-1][h[1]]=jugador*-1
#             if h[1]>0 and self.board[h[0]][h[1]-1]==0 and self.uno_cerca(h[0],h[1]-1):
#                 huecos.append((h[0],h[1]-1))
#                 self.board[h[0]][h[1]-1]=jugador*-1
#                 
# #             print("----------------------------")    
# #             print(self.board)
# #             print(huecos)
# #             print("----------------------------")   
# #         print("Salimos!")
#         return huecos
#                 
#     
#     def huecos_menores(self, jugador): #DONE
# #         print("Huecos menores")
#         for i in range(self.x):
#             for j in range(self.y):
#                 if self.board[i][j]==0 and self.uno_cerca(i, j):
#                     hueco=True
#                     aux_board = np.copy(self.board)
#                     self.board[i][j]=jugador*-1
#                     huecos=self.huecos_menores_busqueda(i,j, jugador)
#                     count=len(huecos)
# #                     print("Total:"+str(count))
# #                     print(huecos)
#                     if count>=5:
#                         if count<=12:
# #                             print(huecos)
# #                             print("Entrando en hueco_real en "+str(i)+","+str(j))
#                             hueco=self.hueco_real(aux_board, huecos)
# #                             print("Es un hueco real?:"+str(hueco))
#                         if hueco:
#                             self.board=aux_board
#                             self.cerrar_hueco(huecos)