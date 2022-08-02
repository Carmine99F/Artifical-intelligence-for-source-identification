from numpy import angle
import centralineModule as cm
import json
import buildInfoCentraline as buildInfo
import triangulationModule as tm
import findCentroide as fc
import time
import angoli
import math
from shapely.geometry import LineString
from shapely.affinity import rotate
import gradiVento as gv
from sympy import Line

arrayCentraline = ['ITCAMMON134567', 'ITCAMMON234567',
                   'ITCAMMON334567', 'ITCAMMON444567']
infoCentraline = {
    "ITCAMMON134567": {
        "lat": 40.821009,
        "lon": 14.810876
    },
    "ITCAMMON234567": {
        "lat": 40.828705,
        "lon": 14.801567
    },
    "ITCAMMON334567": {
        "lat": 40.828199,
        "lon": 14.809813
    },
    "ITCAMMON444567": {
        "lat": 40.824999,
        "lon": 14.819923
    }
}

geovuoto = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "stroke": "#C70039",
            "stroke-width": 2,
            "stroke-opacity": 1,
            "fill": "#00FF00",
            "fill-opacity": 0.5
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [

                ]
            ]
        }
    }, {
        "type": "Feature",
        "properties": {
            "stroke": "#C70039",
            "stroke-width": 3,
            "stroke-opacity": 1,
            "fill": "#FF0000",
            "fill-opacity": 0.5
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [

                ]
            ]
        }
    }
    ]
}
maxCentralina1, maxCentralina2, maxCentralina3 = cm.getMaxCoordinates(
    arrayCentraline, infoCentraline)
#date le coordinate del trinagolo rosso , la funzione restituisce  un dizionario
#con le info relative a
dictAmpiezze= angoli.getAngle_sss(maxCentralina1, maxCentralina2, maxCentralina3, infoCentraline)
# Inseriamo l'intero poligono

for item in arrayCentraline:
    arraycoo = [infoCentraline[item]["lon"], infoCentraline[item]["lat"]]
    geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
geovuoto["features"][0]['geometry']["coordinates"][0].append(
    geovuoto["features"][0]['geometry']["coordinates"][0][0])
# Inseriamo il triangolo rosso
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina1)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina2)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina3)
geovuoto["features"][1]['geometry']["coordinates"][0].append(
    geovuoto["features"][1]['geometry']["coordinates"][0][0])
# Aggiungiamo i punti  sui vertici del poligono
jsonCoordinates = buildInfo.getGeojsonCentralineWithPoints(infoCentraline=infoCentraline,
                                                           geovuoto=geovuoto, dictAmpiezze=dictAmpiezze)

# with open("result_main3/testLinker.geojson","w") as fp:
#     json.dump(jsonCoordinates,fp)


# Otteniamo le coordinate del triangolo col valore massimo, che sarebbe l'ggetto in posizione 1 dell'array features
coordinates = jsonCoordinates["features"][1]["geometry"]["coordinates"][0]
centroid = fc.getCntroide(coordinates)

centerPointTriangle = {
    "type": "Feature",
    "properties": {
        "type_point": "centroide"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
                #centroid[0][0],
                #centroid[0][1]
        ]
    }
}
centerPointTriangle["geometry"]["coordinates"].append(centroid[0][0])
centerPointTriangle["geometry"]["coordinates"].append(centroid[0][1])


cRetta0=centroid[0][0]+0.000000000100
cRetta1=centroid[0][1]+0.000000000100
maxRetta0=maxCentralina1[0]
maxRetta1=maxCentralina1[1]

rettaCentraleTraingolo = {
    "type": "Feature",
    "properties": {
        "type_point": "centroide"
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [
                
            ],
            [
               
            ]
        ]
    }
}
rettaCentraleTraingolo["geometry"]["coordinates"][0].append(cRetta0)
rettaCentraleTraingolo["geometry"]["coordinates"][0].append(cRetta1)
rettaCentraleTraingolo["geometry"]["coordinates"][1].append(maxRetta0)
rettaCentraleTraingolo["geometry"]["coordinates"][1].append(maxRetta1)



ventoDefinitivo = {
    "type": "Feature",
    "properties": {
        "stroke": "#C70039",
        "stroke-width": 3,
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [
                
            ],
             [
                
            ]
        ]
    }
}
point1Lon=maxCentralina1[0]
point1Lat=maxCentralina1[1]+0.010000000000
point2Lon=maxCentralina1[0]
point2Lat=maxCentralina1[1]
ventoDefinitivo["geometry"]["coordinates"][0].append(point1Lon)
ventoDefinitivo["geometry"]["coordinates"][0].append(point1Lat)
ventoDefinitivo["geometry"]["coordinates"][1].append(point2Lon)
ventoDefinitivo["geometry"]["coordinates"][1].append(point2Lat)

gradiVento=gv.getGradiVentoMaxCentraline(geojson=geovuoto,coordinates=maxCentralina1)

linea=LineString([(point1Lon,point1Lat),(point2Lon,point2Lat)]) #retta che dal nord passa  per la centralina max
lineInclinate=rotate(linea,-gradiVento,origin=maxCentralina1) #retta inclinata di  -gradiVento in senso orario

newCoord1=lineInclinate.coords.xy[0].tolist()
newCoord2=lineInclinate.coords.xy[1].tolist()



ventoInclinato = {
    "type": "Feature",
    "properties": {
        "stroke": "#C70039",
        "stroke-width": 3,
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [
                            
            ],
             [
                
            ]
        ]
    }
}
ventoInclinato["geometry"]["coordinates"][0].append(newCoord1[0])
ventoInclinato["geometry"]["coordinates"][0].append(newCoord2[0])
ventoInclinato["geometry"]["coordinates"][1].append(newCoord1[1])
ventoInclinato["geometry"]["coordinates"][1].append(newCoord2[1])

geovuoto["features"].append(centerPointTriangle)
geovuoto["features"].append(rettaCentraleTraingolo)
geovuoto["features"].append(ventoDefinitivo)
geovuoto["features"].append(ventoInclinato)


with open("result_main3/centerPolygon.geojson", "w") as fp:
    json.dump(jsonCoordinates, fp)




linea1=[(newCoord1[0],newCoord2[0]),(newCoord1[1],newCoord2[1])]
line2=[(cRetta0,cRetta1) ,(maxRetta0,maxRetta1)]
gammaAngle=angoli.ang(lineA=linea1,lineB=line2)
print(gammaAngle)

for key in jsonCoordinates["features"]:
    try:
        if key["geometry"]["type"]=="Point":
            print("coord",key["geometry"]["coordinates"])
            if maxCentralina1[0]==key["geometry"]["coordinates"][0] and maxCentralina1[1]==key["geometry"]["coordinates"][1]:
                key["properties"]["gamma_vento"]=gammaAngle
            else:
                pass
                #print("non uguali")
    except Exception as execption:
            pass
with open("result_main3/centerPolygon.geojson", "w") as fp:
    json.dump(jsonCoordinates, fp)
