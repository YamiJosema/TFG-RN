
def especie_lirio(array):
    m = max([(array[i],i) for i in range(3)])
    return m[1]


if __name__=="__main__":
    print especie_lirio([5,15,0])