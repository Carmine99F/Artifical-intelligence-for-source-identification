from typing import List
from math import acos,pi,sqrt


def sss(a:int,b:int,c:int)->int:
    #ritorna l'angolo opposto a un lato a 
    return round(180/pi*acos((b**2 + c**2 - a**2)/(2*b*c)))

def get_angles(a:int,b:int,c:int)->List[int]:
    alpha=sss(a,b,c)
    beta=sss(b,c,a)
    gamma=180-alpha-beta
    return [alpha,beta,gamma]
    
    
if __name__=="__main__":
    print(get_angles(15,5,15))