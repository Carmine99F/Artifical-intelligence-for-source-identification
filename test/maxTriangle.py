from shapely.geometry import Polygon as Poli
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon as Poli
from shapely.ops import triangulate
import numpy as np



def getMaxTraingle(coordinates ,maxCoordinate:list):
    if(len(coordinates)>=2):
        pointsCoordinate=np.array(coordinates)
        
        points = MultiPoint(points=list(pointsCoordinate))
        print("Points ")
        print(points)
        
        poly = Poli([[p.x, p.y] for p in points]) #crea un oggetto Polygon data una serie di coordinate
        #print(poly.wkt)  # prints: 'POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))'
        triangles=triangulate(points)
        arrayTriangles=[]
        
        for triangle in triangles:
            print("Single Triangle")
            print(triangle)
            
            if triangle.within(poly):
                pilitriangle=Poli(triangle)
                print("PiliTriangle")
                print(list(pilitriangle.exterior.coords))
                print(len(list(pilitriangle.exterior.coords)))
                listCoordinateTriangle=list(pilitriangle.exterior.coords)
                #print("Elemento 0")
                #print(type(listCoordinateTriangle[0]))
                print(listCoordinateTriangle)
                print("Arrat in input")
                print(tuple(maxCoordinate))
                if tuple(maxCoordinate) in listCoordinateTriangle:
                    arrayTriangles.append(listCoordinateTriangle)
                    print("Ok ci sono")
                else:
                    print("Non ci sono")
            #arrayTriangles.append(list(pilitriangle.exterior.coords))
            else:
                print("Non è interno")
        array3DTriangles=np.array(arrayTriangles)
        return array3DTriangles
    else:
        return None