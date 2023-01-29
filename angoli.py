from decimal import DivisionByZero
import math
from math import acos,pi,sqrt
"""
    Dopo aver calcolato l'ampiezza di tutti i vertici, costruiamo un json che associa ah ogni nome di centralina
    l'ampizza del proprio angolo interno, mettiamo solo gli angoli delle centraline che rappresentano i 3 valori massimi di pm10
    in parametro infoCentraline è un dizionario che contiene le seguenti informazioniù
    Nome Centralina: {lat e lon}
"""

def lenghtSquare(x,y):
    #print(x," x" , y ," y ")
    xDifference=x[0]-y[0]
    yDifference=x[1]-y[1]
    z=(xDifference*xDifference)+(yDifference*yDifference)
    print("z ",z)
    return z
    
def getAngle_sss(max1,max2,max3,infoCentraline:dict):
    #Quadrati
    print(max1,max2,max3)
    max1Square=lenghtSquare(max2,max3)
    print("max1Square",max1Square)
    max2Square=lenghtSquare(max1,max3)
    max3Square=lenghtSquare(max1,max2)
    
    #Lunghezza dei lati
    max_1=math.sqrt(max1Square)
    max_2=math.sqrt(max2Square)
    max_3=math.sqrt(max3Square)
    #Per la legge del coseno
   
    alpha=math.acos((max2Square+ max3Square - max1Square)/(2*max_2*max_3))
    beta=math.acos((max1Square+ max3Square - max2Square)/(2*max_1*max_3))
    gamma=math.acos((max1Square+ max2Square - max3Square)/(2*max_1*max_2))

    
    alpha = alpha * 180 / math.pi;
    beta = beta * 180 / math.pi;
    gamma = gamma * 180 / math.pi;
    #print("alpha : ",int(alpha))
    #print("beta : " ,int(beta))
    #print("gamma : ",int(gamma))
    
    jsonAngleCentraline={}
    for key,value in infoCentraline.items():
        if value["lon"]==max1[0] and value["lat"]==max1[1]:
            jsonAngleCentraline[key]=int(alpha)
        if value["lon"]==max2[0] and value["lat"]==max2[1]:
            jsonAngleCentraline[key]=int(beta)
        if value["lon"]==max3[0] and value["lat"]==max3[1]:
            jsonAngleCentraline[key]=int(gamma)
    #Il json in output avrà la seguente forma= nomeCentraline:ampiezza angolo
    #print("Json angoli")
    #print(jsonAngleCentraline)
    return jsonAngleCentraline
    
    
"""
Algoritmo per trovare l'ampiezza dell'angolo tra la retta al centro del triangolo 
e quella che passa per la direzione del vento 
"""
    
    
def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value

    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360
    
    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else: 
        return ang_deg
    
