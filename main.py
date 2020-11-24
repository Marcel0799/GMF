import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#--------globaleVariableneinlesen--------
bufferSize = 2

#----Werkstueck--------
blockLength = int(input("Werkstueck Laenge [in cm] : "))
blockWidth = int(input("Werkstueck Breite [in cm] :  "))
blockHeight = int(input("Werkstueck Hoehe [in cm] :  "))

if(blockLength < 0 or blockWidth < 0 or blockHeight<0):
    print("eingaben duerfen nicht negativ sein")
    exit(0)
if(blockHeight>110):
    print("Block wuerde die Maschine beschaedigen, da diese auf Hoehe 110 schneiden soll und der Block groeser ist")
    exit(0)

block = [blockLength,blockWidth,blockHeight]
#-----block fertig-----

#----Werkzeug-------
drillHeight = float(input("Werkzeug Hoehe [in cm] :  "))
drillRad = float(input("Werkzeug Radius [in cm] :  "))

if(drillHeight<=0 or drillRad<=0):
    print("Werkzeug Mase duerfen nicht kleiner oder gleich null sein")
    exit(0)
if(drillHeight > blockHeight):
    print("Werkzeug ist zu gros, es wuerde durch die Grundplatte schneiden")
    exit(0)

drill = [drillHeight,drillRad]
#----Werkzeug fertig----

p1 = [0,-6]
p2 = [120,10]

def distanc(x,y,x1,y1,x2,y2):

    m = (y2-y1)/(x2-x1)
    d = m*x + (y1-m*x)-y
    return d

def createBlock():
    #Hoehenfeldkreieren
    hFeld = np.zeros([block[0]+bufferSize*2,block[1]+bufferSize*2])


    #Hoehenfeldfuellen
    for x in range(block[0]):
        for y in range(block[1]):
            hFeld[x+bufferSize][y+bufferSize]=block[2]

    return hFeld

def mill(hFeld):
    #der fraesprozess an sich

    for x in range(block[0]):
        for y in range(block[1]):
            #korriegierte x und y werte
            xTemp = x + bufferSize
            yTemp = y + bufferSize
            ##der Fraesprozess soll bei (120,10,110) aufhoeren
            #if(xTemp > 120 or yTemp > 10):
            #    continue
            #abstand des aktuellen punktes zur gefraesten gerade
            d = distanc(xTemp,yTemp,p1[0],p1[1],p2[0],p2[1])
            #ist der punkt so nah an der gerade das er im radius des werkzeugsliegt, wird di hoehe verringert
            if(d < drill[1] and d > (-drill[1]) ):
                #die neue hoehe ist die alte hoehe minus die groese des Werkzeugs
                hFeld[xTemp][yTemp] = float(block[2]) - drill[0]

def f(x,y, feld):
    return feld[x,y]

def main():
    #Werkstueck erstellen
    feld = createBlock()


    X = np.arange(0,block[0],1)
    Y = np.arange(0,block[1],1)
    X,Y = np.meshgrid(X,Y)
    Z = f(X,Y, feld)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X=X,Y=Y,Z=Z, cmap=cm.Greens)

    #darstellen des unbehandelten Werkstuecks


    # der Fraesen an sich
    mill(feld)

    X = np.arange(0,block[0],1)
    Y = np.arange(0,block[1],1)
    X,Y = np.meshgrid(X,Y)
    Z = f(X,Y, feld)


    fig = plt.figure()
    ay = fig.add_subplot(111, projection='3d')
    surf = ay.plot_surface(X=X,Y=Y,Z=Z, cmap=cm.Greens)

    plt.show()


if __name__ == "__main__":
    main()
