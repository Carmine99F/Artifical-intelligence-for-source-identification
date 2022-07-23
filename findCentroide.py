from cmath import acos
from random import triangular
from numpy import angle
from shapely.geometry import Polygon as Poli
from shapely.geometry import LineString, MultiLineString
from sympy import Line2D, Mul, Polygon as Poly, sympify
from sympy import Point
from sympy import Triangle
from sympy import sympify
import angoli as angle
import math

def getCntroide(coordinates:list):
    polygon=Poli(coordinates) #non toccare
    x,y=polygon.centroid.xy
    return list(polygon.centroid.coords)
    
    
def all_angle(coordinates:list):
    print(coordinates)
    print(tuple(coordinates[0]))
    linee1=LineString([tuple(coordinates[0]),tuple(coordinates[1])])
    linee2=LineString([tuple(coordinates[1]),tuple(coordinates[2])])
    linee3=LineString([tuple(coordinates[2]),tuple(coordinates[3])])
    #print(linee1.length)
    #print(linee2.length)
    #print(linee3.length)
    l1=linee1.length
    l2=linee2.length
    l3=linee3.length
    print(angle.get_angles(linee1.length,linee2.length,linee3.length))
    print(angle.sss(l1,l2,l3))
    print(angle.sss(l2,l3,l1))
    print(angle.sss(l3,l2,l1))
   
        
        
        
        
        
        

"""    
def getAngle(coordinates:list):
    print("Coordinate")
    print(coordinates)
    p1=coordinates[0]
    p2=coordinates[1]
    p3=coordinates[2]
    trinagle=Triangle(Point(p1),Point(p2),Point(p3))
    print("Triangolo")
    print(trinagle)
    print("Angoli")
    print(trinagle.angles)
    print("Value------")
    print(type(trinagle.angles.values()))
    print(len(trinagle.angles.values()))
    for t in trinagle.angles.values():
        print(acos(t))
        c=complex(acos(t))
        print("Reale")
        print(c.real)
        print(type(acos(t)))
        print(t)
        print(type(t))
    print("Key-----")
    print(trinagle.angles.keys())
    print("Item----")
    print(trinagle.angles.items())
"""    
        