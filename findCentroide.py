
from shapely.geometry import Polygon as Poli
import math

def getCntroide(coordinates:list):
    polygon=Poli(coordinates) 
    x,y=polygon.centroid.xy
    return list(polygon.centroid.coords)
    

        
        
        
        
