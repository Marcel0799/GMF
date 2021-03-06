import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

maxSpeed = float(3000.0/60) # [mm/s]
maxAccelerationX = 8000.0 # [mm/s^2]
maxAccelerationY = 8000.0 # [mm/s^2]
maxAccelerationZ = 5000.0 # [mm/s^2]
#--------globaleVariableneinlesen--------

#----Werkstueck--------
blockLength = 100 #(mm)
blockWidth = 150 #(mm)
blockHeight = 250 #(mm)
block = [blockLength,blockWidth,blockHeight]
#-----Werkstueck fertig-------

#----Werkzeug-------
drillHeight = 20 #(mm)
drillRad = 6 #(mm)
drill = [drillHeight,drillRad]
#----Werkzeug fertig----

#-----Punkte Einlesen------
points = np.empty((0,4))

with open('punkte_klein_time.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        pointX = int(float(row[0]))
        pointY = int(float(row[1]))
        pointZ = int(float(row[2]))
        mSpeed = int(float(row[3])/60)
        points = np.r_[points, [[pointX,pointY,pointZ,mSpeed]]]

print(len(points))
for i in range(0,len(points)):
    print(points[i])  
#------Ende der Punkt Eingabe-----------

def calcNormVec(point1,point2):
    vec = np.zeros(3)
    vec[0] = point2[0]-point1[0]
    vec[1] = point2[1]-point1[1]
    vec[2] = point2[2]-point1[2]
    length = np.sqrt( (vec[0]**(2)) + (vec[1]**(2)) + (vec[2]**(2)) )
    normVec = np.zeros(3)
    normVec[0] = vec[0]/length
    normVec[1] = vec[1]/length
    normVec[2] = vec[2]/length 
    normLength = np.sqrt( (normVec[0]**(2)) + (normVec[1]**(2)) + (normVec[2]**(2)) )
    return normVec

def calcVecLen(point1,point2):
    vec = np.zeros(3)
    vec[0] = point2[0]-point1[0]
    vec[1] = point2[1]-point1[1]
    vec[2] = point2[2]-point1[2]
    length = np.sqrt( (vec[0]**(2)) + (vec[1]**(2)) + (vec[2]**(2)) )
    return length

def main():
    time = 0.0
    #allSpeeds = [0.0]

    for i in range(len(points)):
        #speedList = [0.0] 
        oneTime = 0.0
        lastSpeedX = 0.0
        lastSpeedY = 0.0
        lastSpeedZ = 0.0
        maxSpeed = points[i,3]
        if(i==0):
            continue
        normVec = calcNormVec(points[i-1],points[i])
        normVec[0] = np.abs(normVec[0])
        normVec[1] = np.abs(normVec[1])
        normVec[2] = np.abs(normVec[2])
        length = calcVecLen(points[i-1],points[i])
        
        for y in range(int((length+1)/2)):
            # fuer jeden iterativen Fraess Schritt, welcher jeweils 1mm laenge hat, wird hier die maximal erlaubte geschwindkeit berechnet
            
            curSpeedX = maxSpeed
            curSpeedY = maxSpeed
            curSpeedZ = maxSpeed
            print("Der " + str(y) + " Schritt")
            if(normVec[0] != 0.0):
                XnegP = (lastSpeedX / normVec[0])
                XnegQ = (maxAccelerationX / normVec[0])
                curSpeedX = ( (XnegP/2) + np.sqrt( ((XnegP/2)**(2)) + XnegQ ) )
                print("Maximale Geschw. das die Besch. der X-Achse nicht ueberschritten wird :" + str(curSpeedX))

            if(normVec[1] != 0.0):
                YnegP = (lastSpeedY / normVec[1])
                YnegQ = (maxAccelerationY / normVec[1])
                curSpeedY = ( (YnegP/2) + np.sqrt( ((YnegP/2)**(2)) + YnegQ ) )
                print("Maximale Geschw. das die Besch. der Y-Achse nicht ueberschritten wird " + str(curSpeedY))

            if(normVec[2] != 0.0):
                ZnegP = (lastSpeedZ / normVec[2])
                ZnegQ = (maxAccelerationZ / normVec[2])
                curSpeedZ = ( (ZnegP/2) + np.sqrt( ((ZnegP/2)**(2)) + ZnegQ ) )
                print("Maximale Geschw. das die Besch. der Z-Achse nicht ueberschritten wird " + str(curSpeedZ))

            realSpeed = min(curSpeedX,curSpeedY,curSpeedZ,maxSpeed)

            lastSpeedX = normVec[0] / (1/realSpeed)
            lastSpeedY = normVec[1] / (1/realSpeed)
            lastSpeedZ = normVec[2] / (1/realSpeed)

            print("gewaehlte Gesch: " + str(realSpeed))
            #speedList.append(float(realSpeed))
            oneTime = oneTime + (1/realSpeed)

            print("-------------------------------------")
        oneTime = oneTime*2
        time = time + oneTime

        #----------------List bearbeiten-------------
        #laenge = len(speedList)-1
        #for h in range(laenge):
        #    speedList.append(speedList[laenge-h])
        #allSpeeds += speedList
        #-----------------List------------------
        print("die benötigte Zeit für diese Gerade = " + str(oneTime) + " sekunden, die Gerade war " + str(length) + "mm lang" )

    print("Insgesamt dauert das Fraessen: " + str(time) + " sekunden")
    #allSpeeds.append(0.0)
    #plt.plot(allSpeeds)
    #plt.savefig("image1.png")

if __name__ == "__main__":
    main()
