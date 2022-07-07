from sympy import li
import requestInformation as ri
import time
import  json


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
# geovuoto={
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {
#       },
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
            
#           ]
#         ]
#       }
#     }
#   ]
# }


#Per ogni nome delle centraline prendiamo le infotmazioni realtive  al vento e al pm
#Mettiamo ogni oggetto json che ci viene restituito in un array
#dictInfoCentraline=[]
jsonCentraline={}
listPm10=[]
for item in arrayCentraline:
    #print(item)
    #ci prendiamo lat e lon dal backend per ogni sensore
    #arraycoo=[infoCentraline[item]["lon"],infoCentraline[item]["lat"]]
    #geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
    objectInfo= ri.getInfo(item) #contiene la lista dei valori lkegati al pm e al vento senza il nome della centralina
    #print("Type objectInfo",type(objectInfo))
    #print(objectInfo)
    if objectInfo is not None:
        print("Pm10")
        print(objectInfo["pm10"])
        listPm10.append(objectInfo["pm10"])
        #centralina={item : objectInfo}
        #dictInfoCentraline.append(centralina)
        jsonCentraline.update({item:objectInfo})

#controlliamo se almeno uno dei valori del pm10 è maggiore di 50
if any(i >50 for i in listPm10):
    print("Ok c'è un elemento maggiore di 50")
else:
    print("Non c'è nessun elemento maggiore di 50")

print("JsonCentraline")
print(json.dumps(jsonCentraline,indent=4))
print("---------------------------------------------------------")

    

#trovare quello con pm10 Massimo
maxPm10=list(jsonCentraline.values())[0]["pm10"]
#maxPm10=jsonCentraline[arrayCentraline[0]]["pm10"]
maxKey=list(jsonCentraline.keys())[0]

print("MaxKey ",maxKey)
print("MaxPM10",maxPm10)


for keyCentraline,objectInfo in jsonCentraline.items():
    if(objectInfo["pm10"])>maxPm10:
        maxPm10=objectInfo["pm10"]
        maxKey=keyCentraline
    #print(keyCentraline)
    #print(objectInfo["pm10"])
print("Centralina con maggior esposizione al pm10 ", maxKey)

#trovare lan e long della centralina col valore massimo
coordinateMax=[infoCentraline[maxKey]["lon"],infoCentraline[maxKey]["lat"]]
print(coordinateMax)

    




#geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
#print(geovuoto)


#with open("testauto.geojson","w") as fp:
    #json.dump(geovuoto,fp)
    

def getMaxCoordinates():
    print("coordnateMax vale ")
    print(coordinateMax)
    return coordinateMax