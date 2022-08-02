import math
from typing import List
from math import acos,pi,sqrt
"""
    Dopo aver calcolato l'ampiezza di tutti i vertici, costruiamo un json che associa ah ogni nome di centralina
    l'ampizza del proprio angolo interno, mettiamo solo gli angoli delle centraline che rappretano i 3 valori massimi di pm10
"""

def lenghtSquare(x,y):
    xDifference=x[0]-y[0]
    yDifference=x[1]-y[1]
    z=(xDifference*xDifference)+(yDifference*yDifference)
    return z
    
def getAngle_sss(max1,max2,max3,infoCentraline:dict):
    #Quadrati
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
         
    print(jsonAngleCentraline)
    return jsonAngleCentraline
    
    
