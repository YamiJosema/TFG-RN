import os
import csv

Formas=["F","I","L","N","P","T","U","V","W","X","Y","Z"]

def cargar_pentominos():
    pentominos=[]
    if os.path.isfile('csv/pentominos.csv')==False:
        crear_pentominos_csv()
    
    with open('csv/pentominos.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            pentominos.append(row)
    return pentominos


def crear_pentominos_csv():
    no_inversa=["T","U","V","W"]
    with open('csv/pentominos.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in Formas:
            if i=="X":
                filewriter.writerow(["X",0,0])
            elif i=="I":
                filewriter.writerow(["I",0, 0])
                filewriter.writerow(["I",1, 0])
            elif i=="Z":
                filewriter.writerow(["Z",0, 0])
                filewriter.writerow(["Z",1, 0])
                filewriter.writerow(["Z",0, 1])
                filewriter.writerow(["Z",1, 1])
            else:
                for j in range(4):
                    filewriter.writerow([i,j,0])
                    if i not in no_inversa:
                        filewriter.writerow([i,j,1])