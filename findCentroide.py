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
    polygon=Poli(coordinates) 
    x,y=polygon.centroid.xy
    return list(polygon.centroid.coords)
    
"""
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
        
        
        
        
        
        
