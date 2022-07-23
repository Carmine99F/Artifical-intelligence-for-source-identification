import centralineModule as cm
import json
import buildInfoCentraline as buildInfo
import triangulationModule as tm
import findCentroide as fc
import time

arrayCentraline=['ITCAMMON134567','ITCAMMON234567','ITCAMMON334567','ITCAMMON444567']
infoCentraline={
     "ITCAMMON134567":{
         "lat":40.821009,
         "lon":14.810876
     },
     "ITCAMMON234567":{  
         "lat": 40.828705,
         "lon": 14.801567
     },
     "ITCAMMON334567":{
         "lat": 40.828199,
         "lon": 14.809813
     },
     "ITCAMMON444567":{
         "lat": 40.824999,
         "lon": 14.819923
     }
}
maxCentralina1,maxCentralina2,maxCentralina3=cm.getMaxCoordinates(arrayCentraline,infoCentraline)

geovuoto={
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
#Inseriamo l'intero poligono
for item in arrayCentraline:
     arraycoo=[infoCentraline[item]["lon"],infoCentraline[item]["lat"]]
     geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
#Inseriamo il triangolo rosso
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina1)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina2)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina3)
geovuoto["features"][1]['geometry']["coordinates"][0].append(geovuoto["features"][1]['geometry']["coordinates"][0][0])
#Aggiungiamo i punti  sui vertici del poligono
jsonCoordinates=buildInfo.getGeojsonCentralineWithPoints(infoCentraline=infoCentraline,geovuoto=geovuoto)

#with open("result_main3/testLinker.geojson","w") as fp:
#     json.dump(jsonCoordinates,fp)



coordinates=jsonCoordinates["features"][1]["geometry"]["coordinates"][0]

centroid=fc.getCntroide(coordinates)



center={
      "type": "Feature",
      "properties": {          
        },
        "geometry": {
        "type": "Point",
          "coordinates": [
                centroid[0][0],
                centroid[0][1]
              ]
            }
        }

geovuoto["features"].append(center)
#print(geovuoto)

with open("result_main3/centerPolygon.geojson","w") as fp:
     json.dump(jsonCoordinates,fp)
     
fc.all_angle(coordinates)