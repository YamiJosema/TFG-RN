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