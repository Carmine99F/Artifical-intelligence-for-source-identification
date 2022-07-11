import numpy as np
from shapely.geometry import Polygon as Poli


def getMaxTraingle(listTriangle : np.ndarray,c1:list,c2:license,c3:list):
    listTriangle=listTriangle.tolist()
    arrayTriangle=[]
    for triangle in listTriangle:
        pilitriangle=Poli(triangle)
        listCoordinate=list(pilitriangle.exterior.coords)
        if tuple(c1) in listCoordinate and tuple(c2) in listCoordinate and tuple(c3) in listCoordinate:
            arrayTriangle.append(listCoordinate)
    if len(arrayTriangle) >0:
        arrayTriangle=np.array(arrayTriangle)
        return arrayTriangle
    else:
        return None