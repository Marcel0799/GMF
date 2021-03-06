
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

#-----Test einstellungen#
testSettings = False
if (len(sys.argv)>1):
    testSettings = True

#--------globaleVariableneinlesen--------
if (not testSettings):
    try:
        #----Werkstueck--------
        blockLength, blockWidth, blockHeight = input("Werkstueck Laenge, Breite, Hoehe angeben [in mm] : ").split()
        blockLength = int(blockLength)
        blockWidth = int(blockWidth)
        blockHeight = int(blockHeight)
        
        if(blockLength < 0 or blockWidth < 0 or blockHeight<0):
            print("eingaben duerfen nicht negativ sein")
            exit(0)
        if(blockHeight>1100):
            print("Block wuerde die Maschine beschaedigen, da diese auf Hoehe 110 schneiden soll und der Block groeser ist")
            exit(0)
            
        block = [blockLength,blockWidth,blockHeight]
        #-----Werkstueck fertig-------
        
        #----Werkzeug-------
        drillHeight, drillRad = input("Werkzeug Hoehe Radius [in mm] : ").split()
        drillHeight = int(drillHeight)
        drillRad = int(drillRad)

        if(drillHeight<=0 or drillRad<=0):
            print("Werkzeug Mase duerfen nicht kleiner oder gleich null sein")
            exit(0)
        if(drillHeight > blockHeight):
            print("Werkzeug ist zu gros, es wuerde durch die Grundplatte schneiden")
            exit(0)

        drill = [drillHeight,drillRad]
        #----Werkzeug fertig----
        
    except ValueError:
        print("Value exception")
        exit(1)
    except:
        print("generell Exception")
else:
    block = [100,100,100]
    drill = [50,10]

#-----Punkte Einlesen------
if(not testSettings):
    points = np.empty((0,3))
    try:
        while(True):
            pointX, pointY, pointZ = input(str(len(points)+1) + ".Punkt [x y z]: ").split()
            pointX = int(pointX)
            pointY = int(pointY)
            pointZ = int(pointZ)
            #if(pointX<0 or pointY<0 or pointY<0):
            #    print("Der gewaehlte Punkt darf nicht negativ sein")
            #    exit(0)
            #if(pointX>blockLength or pointY>blockWidth or pointY>blockHeight):
            #    print("Der gewaehlte Punkt ist groesser als das Werkstueck")
            #   exit(0)
            points = np.r_[points, [[pointX,pointY,pointZ]]]
            print(points)
    except ValueError:
        print("Ende der Eingabe, es wurden " + str(len(points)) + " eingegeben")
        #ende der eingabe
    except:
        print("es ist ein fehler aufgetreten")
        exit(0)
        
    if(len(points) <= 0):
        print("Sie haben keine Punkte eingegeben")
        exit(0)
        
else:
     points = np.array([[20,20,90],[80,20,60],[80,80,40],[10,90,75]])
  
#------Ende der Punkt Eingabe-----------


def distance(p1,p2):
    return np.linalg.norm(p2-p1)

    
#Gibt den Punkt auf der Strecke von p1 nach p2 zurück, welcher in x,y Dimension am wenigsten Abstand zu a hat.
#In der Ausgabe hat der Punkt jedoch eine Z-Koordinate
def nearestPointNoZ(p1,p2,a):
    #das gleiche wie nearest Point, nur in x&y Dimension
    p1p2 = p2-p1
    #Line:
    #x = (p2-p1) * t + p1
    
    nP = nearestPoint(p1[:2],p2[:2], a[:2])
    t = 0
    #get Z für nearestPoint
    if(p1p2[0] != 0):
        t = (nP[0]-p1[0])/p1p2[0]
    if(p1p2[1] != 0):
        t = (nP[1]-p1[1])/p1p2[1]
    z = p1p2[2]*max(0,min(1,t)) + p1[2]
    nP = np.append(nP,z)
    return nP
    
# Gibt den nächsten Punkt zu a auf der Strecke P1-P2
def nearestPoint(p1,p2,a):
    p1p2 = p2-p1
    #Line:
    #x = (p2-p1)* t + p1
    #Plane:
    #0 = (p2-p1) 'dot' (x-a)
    #(p2-p1)'dot'(a) = (p2-p1)'dot'(x)
    #Line 'X' Plane
    #(p2-p1)'dot'(a) = (p2-p1)'dot'((p2-p1)* t + p1)
    #(p2-p1)'dot'(a) = (p2-p1)'dot'((p2-p1)* t) + (p2-p1)'dot'(p1)
    #(p2-p1)'dot'(a) - (p2-p1)'dot'(p1) = (p2-p1)'dot'((p2-p1)* t)
    #(p2-p1)'dot'(a) - (p2-p1)'dot'(p1) = (p2[0]-p1[0])^2 * t + (p2[1]-p1[1])^2 * t + (p2[2]-p1[2])^2 *t
    #(p2-p1)'dot'(a) - (p2-p1)'dot'(p1) =((p2[0]-p1[0])^2+(p2[1]-p1[1])^2+(p2[2]-p1[2])^2) * t
    #t =((p2-p1)'dot'(a) - (p2-p1)'dot'(p1)) /((p2[0]-p1[0])^2+(p2[1]-p1[1])^2+(p2[2]-p1[2])^2)
    #           d                   f                               g
    
    #t =(np.dot(p2-p1,a) - np.dot(p2-p1,p1)) /((p2[0]-p1[0])^2+(p2[1]-p1[1])^2+(p2[2]-p1[2])^2)
    d = np.dot(p1p2,a)
    f = np.dot(p1p2,p1)
    g = np.dot(p1p2,p1p2)
    t = (d-f)/g
    return ((p2-p1)* max(0,min(1,t)) + p1)

def createBlock():
    #Hoehenfeldkreieren
    hFeld = np.zeros([block[0],block[1]])


    #Hoehenfeldfuellen
    for x in range(block[0]):
        for y in range(block[1]):
            hFeld[x][y]=block[2]

    return hFeld

def mill(hFeld):
    #der fraesprozess an sich

    for x in range(block[0]):
        for y in range(block[1]):
            #korriegierte x und y werte
            
            a = np.array([x,y,hFeld[x][y]])
            
            #Fuer alle aus den Punkten enstehenden Geraden wird gefrast
            for i in range(len(points)) :
                if(i != 0):
                
                    n = points[i]-points[i-1]
                    #for i in range(len(n)):
                    #    n[i] *= 1/(np.linalg.norm(n))
                        
                        
                    ##Nachster Punkt auf Gerade von beliebigem Punkt a durch Schnittpunkt mit Ebene
                    #Ebene durch a mit normalen n ist :
                    # n[0]*x + n[1]*x2 + n[2]*x3 = d
                    #gerade = n * t + points[i-1]
                    
                    #n[0]*(n[0] * t + points[i-1][0]) +
                    #n[1]*(n[1] * t + points[i-1][1]) +
                    #n[2]*(n[2] * t + points[i-1][2]) = d
                    #(n dot n)  * t + n dot points[i-1] = d
                    # (np.dot(n,a)- np.dot(n,points[i-1]))/ np.dot(n,n) = t
                    
                    
                    #Punkt auf der Geraden, welcher am nachsten am punkt a liegt.
                    #ta = (np.dot(n,a)-np.dot(n,points[i-1]))/ np.dot(n,n)
                    #ta = (n[0]*a[0]+n[1]*a[1]- n[0]*points[i-1][0]-n[1]*points[i-1][1])/(n[0]^2 + n[1]^2)
                    
                    #cutPoint = n * ta + points[i-1]
                    cutPoint = nearestPointNoZ(points[i-1],points[i],a)
                    
                    #abstand des aktuellen punktes zur gefraesten gerade
                    
                    dis = distance(a[:2],cutPoint[:2])
                    
                    #if(np.array_equal(a,np.array([80,60,hFeld[80][60]]))):
                     #   print(a)
                    #    print(cutPoint)
                    #    print(dis)
                        
                    #dis = distanc(xTemp,yTemp,points[i-1][0],points[i-1][1],points[i][0],points[i][1])
                    #ist der punkt so nah an der gerade das er im radius des werkzeugsliegt, wird di hoehe verringert
                    if(dis < drill[1]):
                        #die neue hoehe ist die Höhe auf dem Das Werkzeug bewegt wird, oder die aktuelle Höhe vom Werkstück
                        hFeld[x][y] = min([cutPoint[2],hFeld[x][y]])

def f(x,y, feld):
    return feld[x,y]

def main():
    #Werkstueck erstellen
    feld = createBlock()

    #darstellen des unbehandelten Werkstuecks


    # der Fraesen an sich
    mill(feld)

    X = np.arange(0,block[0],1)
    Y = np.arange(0,block[1],1)
    X,Y = np.meshgrid(X,Y)
    Z = f(X,Y, feld)

    #Transperent colors
    # get colormap
    ncolors = 256
    color_array = plt.get_cmap('inferno')(range(ncolors))

    # change alpha values
    color_array[:,-1] = np.linspace(0.5,1,ncolors)

    # create a colormap object
    cmap = LinearSegmentedColormap.from_list(name='rainbow_alpha',colors=color_array)

    # register this new colormap with matplotlib

    plt.register_cmap(cmap=cmap)
    
    
    fig = plt.figure()
    ay = fig.add_subplot(111, projection='3d')
    surf = ay.plot_surface(X=X,Y=Y,Z=Z, cmap='rainbow_alpha')
    for i in range(len(points)) :
        if(i != 0):
            ay.plot(np.array([points[i-1][0],points[i][0]])
                ,np.array([points[i-1][1],points[i][1]]),
                np.array([points[i-1][2],points[i][2]]))

    plt.show()


if __name__ == "__main__":
    main()
