from random import choice
# from sklearn.neurla_network import MLPClassifier

options = ["piedra", "tijeras", "papel"]
def search_winner(p1,p2):
    if p1 == p2:
        result = 0
    elif p1 == "piedra" and p2 == "tijeras":
        result = 1
    elif p1=="piedra" and p2 == "papel":
        result = 2
    elif p1=="tijeras" and p2=="piedra":
        result=2
    elif p1=="tijeras" and p2=="papel":
        result=1
    elif p1=="papel" and p2=="tijeras":
        result=2
    elif p1=="papel" and p2=="piedra":
        result=1
    
    return result

def get_choices():
    return choice(options)


def str_to_list(option):
    if option=="piedra":
        res = [1,0,0]
    elif option=="tijeras":
        res = [0,1,0]
    else:
        res=[0,0,1]
    return res


def main():
    data_x=list(map(str_to_list, ["piedra","tijeras","papel"]))
    data_y=list(map(str_to_list, ["papel","piedra","tijeras"]))
    
    print data_x
    print data_y
    
    


if __name__=="__main__":
    main()
#     print search_winner("piedra", "piedra")
#     for i in range(10):
#         p1= get_choices()
#         p2=get_choices()
#         print "Player1 "+p1+", Player2 "+p2+", Winner "+str(search_winner(p1, p2))