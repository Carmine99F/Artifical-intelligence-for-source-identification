from numpy import inf
import requestInformation as ri
import json



"""_summary_
Al geojson in input aggiunge gli oggetti che rappresentano i punti dei vertici
 """
def getGeojsonCentralineWithPoints(infoCentraline:dict,geovuoto:dict):
  for key,value in infoCentraline.items():
    dictInfoKey=ri.getInfo(key)
    if dictInfoKey is not None:
        formatNewData={
            "type": "Feature",
            "properties": dictInfoKey,
            "geometry": {
                "type": "Point",
                "coordinates": [
                    value["lon"],
                    value["lat"]
                    ]
                }
            }
        geovuoto["features"].append(formatNewData)
    else:
        formatNewData={
            "type": "Feature",
            "properties": {
                
                },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    value["lon"],
                    value["lat"]
                ]
            }
        }
        geovuoto["features"].append(formatNewData)
  return geovuoto
              

      

"""
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
     #Da qui in poi si dovrebbero aggiungere i nuovi dati
   ]
 }

formatNewData={
      "type": "Feature",
      "properties": {
        
        },
      "geometry": {
        "type": "Point",
        #"coordinates": [
          
        #]
      }
    }

dictInfoCentraline=[]
for item in arrayCentraline:
     print(item)
     #ci prendiamo lat e lon dal backend per ogni sensore
     arraycoo=[infoCentraline[item]["lon"],infoCentraline[item]["lat"]]
     geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
    
geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
print("Start loop")

for key,value in infoCentraline.items():
    dictInfoKey=ri.getInfo(key)
    newFormat=formatNewData
    if dictInfoKey is not None:
        #print(type(dictInfoKey))
        #print(dictInfoKey.keys())
        print("Dict info key")
        print(dictInfoKey)
        #print(dictInfoKey)
        
        #newFormat=formatNewData
        #print(newFormat)
    
        #arrayCoordinate=[value["lon"],value["lat"]]
        #newFormat["properties"].update(dictInfoKey)
        #newFormat["geometry"].update({"coordinates":arrayCoordinate})
        #geovuoto["features"].append(newFormat)

        formatNewData={
            "type": "Feature",
            "properties": dictInfoKey,
            "geometry": {
                "type": "Point",
                "coordinates": [
                    value["lon"],
                    value["lat"]
                    ]
                }
            }
        geovuoto["features"].append(formatNewData)        
        #newFormat.clear()
        #formatNewData["properties"].update({"Chaive":dictInfoKey["pm10"]})
        print("Format Data")
        print(newFormat)
        print("Geo vuoto")
        print(json.dumps(geovuoto,indent=4))
    else:
        formatNewData={
            "type": "Feature",
            "properties": {
                
                },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    value["lon"],
                    value["lat"]
                ]
            }
        }
        geovuoto["features"].append(formatNewData)        
"""
        
