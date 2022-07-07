import json
from textwrap import indent
from urllib import response
import triangulationModule as tm 
import geojson
import requests
import time 
import requestInformation
import maxTriangle as mt
import centralineModule as centraline


#arrayCentraline=['ITCAMMON134567','ITCAMMON334567','ITCAMMON444567']
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


dictInfoCentraline=[]
for item in arrayCentraline:
     print(item)
     #ci prendiamo lat e lon dal backend per ogni sensore
     arraycoo=[infoCentraline[item]["lon"],infoCentraline[item]["lat"]]
     geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
    
geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
# print(geovuoto)

#########################################################################################


directory="coordinates/"
filename="ProvaMax.geojson"
locationFile=directory+""+filename

#with open(locationFile,"r") as f:
      #jsonCoordinates=json.load(f)

jsonCoordinates=geovuoto  

# with open("testauto.geojson","w") as fp:
#     json.dump(jsonCoordinates,fp)
      
features=(jsonCoordinates["features"][0])
geometry=features["geometry"]
coordinates=geometry["coordinates"][0]

listTraingles=tm.traingulatePolygon(coordinates)
#maxCentraline=centraline.getMaxCoordinates()
maxCentraline=centraline.getMaxCoordinates(arrayCentraline,infoCentraline)
print("Max centraline : ",maxCentraline)
print(type(maxCentraline))
#listTraingles=mt.getMaxTraingle(coordinates,maxCentraline)

if listTraingles is not None:
    print("Triangoli")
    print(type(listTraingles))
    print(listTraingles)
    #print("Array non vuoto",type(listTraingles))
    geoJsonObject= {"type":"FeatureCollection","features":
                [
                    {
                        "type":"Feature","properties":
                            {"stroke":"#C70039","stroke-width":2,"stroke-opacity":1,"fill":"#BEF655","fill-opacity":0.5},
                        "geometry":{"type":"Polygon","coordinates":listTraingles.tolist()}
                    }
                ]
            }

    #print(type(geoJsonObject))
    #print(geoJsonObject.__str__().replace("'", '"'))
    #outputfile=str(filename).replace("coordinates","result")
    #print("Output File",outputfile)
    outputfile="result/"+filename.split(".")[0] + "mod.geojson"
    print(outputfile)
    #outputfile=filename.split(".")[0] + "mod.geojson"
    try:
        with open(outputfile,'w') as f:
            f.write(str(geoJsonObject.__str__().replace("'", '"')))
    except Exception as ex:
        print(str(ex))
else:
    print("None")
