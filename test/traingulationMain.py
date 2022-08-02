import json
from textwrap import indent
from urllib import response
import triangulationModule as tm 
import geojson
import time 
import centralineModule as centraline
import maxTriangleByCentraline as mtbc


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



directory="coordinates/"
filename="ProvaMax.geojson"
locationFile=directory+""+filename

#with open(locationFile,"r") as f:
      #jsonCoordinates=json.load(f)

jsonCoordinates=geovuoto  

with open("testauto.geojson","w") as fp:
     json.dump(jsonCoordinates,fp)
      
features=(jsonCoordinates["features"][0])
geometry=features["geometry"]
coordinates=geometry["coordinates"][0]

#listTraingles=tm.traingulatePolygon(coordinates)
#maxCentralina1=centraline.getMaxCoordinates()
maxCentralina1 , maxCentralina2,maxCentralina3=centraline.getMaxCoordinates(arrayCentraline,infoCentraline)
if maxCentralina1 is not None and maxCentralina2 is not None and maxCentralina3 is not None:
    listTraingles=tm.traingulatePolygon(coordinates)
    triangleMaxPM10=mtbc.getMaxTraingle(listTraingles,maxCentralina1,maxCentralina2,maxCentralina3)


    if listTraingles is not None:
        geoJsonObject1= {"type":"FeatureCollection","features":
                    [
                        {
                            "type":"Feature","properties":
                                {"stroke":"#C70039","stroke-width":2,"stroke-opacity":1,"fill":"#00FF00","fill-opacity":0.5},
                            "geometry":{"type":"Polygon","coordinates":listTraingles.tolist()}
                        }
                    ]
                }
    if triangleMaxPM10 is not None:
        geoJsonObject2= {"type":"FeatureCollection","features":
                    [
                        {
                            "type":"Feature","properties":
                                {"stroke":"#C70039","stroke-width":2,"stroke-opacity":1,"fill":"#FF0000","fill-opacity":0.5},
                            "geometry":{"type":"Polygon","coordinates":triangleMaxPM10.tolist()}
                        }
                    ]
                }
        
        outputfile1="result/"+filename.split(".")[0] + "mod.geojson"
        outputfile2="result/"+filename.split(".")[0] + "modMaxCentraline.geojson"

        print(outputfile1)
        #outputfile=filename.split(".")[0] + "mod.geojson"
        try:
            with open(outputfile1,'w') as f:
                f.write(str(geoJsonObject1.__str__().replace("'", '"')))
            with open(outputfile2,'w') as f:
                f.write(str(geoJsonObject2.__str__().replace("'", '"')))
        except Exception as ex:
            print(str(ex))
    else:
        print("None")
