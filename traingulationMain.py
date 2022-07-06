import json
from textwrap import indent
from urllib import response
import triangulationModule as tm 
import geojson
import requests
import time 
import requestInformation

# url="https://square.sensesquare.eu:5001/download"
# dati={
#     "apikey":"4BSFRYMNPZ0J",
#     "req_type":"hourly",
#     "zoom":5,
#     "start_hour":0,
#     "end_hour":23,
#     "format":"json",
#     "fonti":"ssq",
#     "req_centr":"ITCAMMON134567",
#     "start_date":"2022-03-27",
#     "end_date":"2022-03-27"
# }

# response=requests.post(url,data=dati)
# print(response.status_code)
# print(response.text)
# time.sleep(3000)


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
geovuoto={
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
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

for item in arrayCentraline:

    #ci prendiamo lat e lon dal backend per ogni sensore
    arraycoo=[infoCentraline[item]["lon"],infoCentraline[item]["lat"]]
    geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
    
geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
print(geovuoto)

directory="coordinates/"
filename="cosenza.geojson"
locationFile=directory+""+filename

# with open(locationFile,"r") as f:
#     jsonCoordinates=json.load(f)
jsonCoordinates=geovuoto  

with open("testauto.geojson","w") as fp:
    json.dump(jsonCoordinates,fp)
      
features=(jsonCoordinates["features"][0])
geometry=features["geometry"]
coordinates=geometry["coordinates"][0]

listTraingles=tm.traingulatePolygon(coordinates)

if listTraingles is not None:
    #print("Array non vuoto",type(listTraingles))
    geoJsonObject= {"type":"FeatureCollection","features":
                [
                    {
                        "type":"Feature","properties":
                            {"stroke":"#ff0000","stroke-width":2,"stroke-opacity":1,"fill":"#555555","fill-opacity":0.5},
                        "geometry":{"type":"Polygon","coordinates":listTraingles.tolist()}
                    }
                ]
            }

    #print(type(geoJsonObject))
    #print(geoJsonObject.__str__().replace("'", '"'))
    #outputfile=str(filename).replace("coordinates","result")
    #print("Output File",outputfile)
    outputfile="result/"+filename.split(".")[0] + "mod.geojson"
    #outputfile=filename.split(".")[0] + "mod.geojson"
    try:
        with open(outputfile,'w') as f:
            f.write(str(geoJsonObject.__str__().replace("'", '"')))
    except Exception as ex:
        print(str(ex))
else:
    print("None")
