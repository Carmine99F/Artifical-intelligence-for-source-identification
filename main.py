import centralineModule as cm
import json
import buildInfoCentraline as buildInfo
import findCentroide as fc
import angoli
import math
#import shapely.affinity
from shapely.geometry import Point,Polygon
from shapely.geometry import LineString
from shapely.affinity import rotate
import gradiVento as gv
import config
import geojson
import requests
import hourlyAverages as ha
import rette
import requestInformation as ri
import calcoloProbabilità as cp
import time



arrayCentraline = config.arrayNomiCentraline

infoCentraline={}
for nameCentraline in arrayCentraline:
    re= requests.post("https://square.sensesquare.eu:5002/informazioni_centralina", 
                      data={"apikey": "WDBNX4IUF66C", "ID": nameCentraline})
    #print(re.text)
    infoCentraline[nameCentraline]={}
    infoCentraline[nameCentraline]['lat']= re.json()['result']['lat']
    infoCentraline[nameCentraline]['lon']= re.json()['result']['lon']
    
#print(infoCentraline)

geovuoto=geojson.geovuoto
arrayPointTriangle=[]



ri.getInfo2(arrayCentraline)
maxCentralina1, maxCentralina2, maxCentralina3 = cm.getMaxCoordinates2(arrayCentraline, infoCentraline)
idCentrRedMesh=[config.nomeCentralina1,config.nomeCentralina2,config.nomeCentralina3]

ha.getInfo(arrayCentraline)
pg=cp.dailyPercentage(idCentrRedMesh)
config.dizMediaGiornaliera[config.nomeCentralina1]["percentuale_giornaliera"]=pg
config.dizMediaGiornaliera[config.nomeCentralina2]["percentuale_giornaliera"]=pg
config.dizMediaGiornaliera[config.nomeCentralina3]["percentuale_giornaliera"]=pg

#print(json.dumps(config.dizMediaGiornaliera,indent=3))



#maxCentralina1, maxCentralina2, maxCentralina3 = cm.getMaxCoordinates(arrayCentraline, infoCentraline)
#print("maxC1",maxCentralina1)
#print("maxC2",maxCentralina2)
#print("maxC3",maxCentralina3)

#time.sleep(5000)



#date le coordinate del trinagolo rosso , la funzione restituisce  un dizionario con le info relative agli angoli
dictAmpiezze= angoli.getAngle_sss(maxCentralina1, maxCentralina2, maxCentralina3, infoCentraline)




S=math.pow(10,3)
p=1.25*(math.pow(10,3))
sp=S*p
div=sp/config.valueMaxPm10
dp=int(math.sqrt((div)))

# Inseriamo l'intero poligono
for key,item in config.dizMediaGiornaliera.items():
    print("item")
    print(json.dumps(item,indent=3))
    print("-----------------------")
    #print("key ",key)
    arraycoo=[ item["lon"],item["lat"]]
    arrayPointTriangle.append(tuple(arraycoo))
    geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
    
"""
for item in arrayCentraline:
    arraycoo = [infoCentraline[item]["lon"], infoCentraline[item]["lat"]]
    arrayPointTriangle.append(tuple(arraycoo))
    geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
"""    
geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
arrayPointTriangle.append(arrayPointTriangle[0])
#print(arrayPointTriangle)
triangle=Polygon(arrayPointTriangle)
# Inseriamo il triangolo rosso
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina1)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina2)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina3)
geovuoto["features"][1]['geometry']["coordinates"][0].append(geovuoto["features"][1]['geometry']["coordinates"][0][0])

#print("Max centraline 1",list(maxCentralina1))
# Aggiungiamo i punti  sui vertici del poligono
jsonCoordinates = buildInfo.getGeojsonCentralineWithPoints2(infoCentraline=infoCentraline,
                                                           geovuoto=geovuoto, dictAmpiezze=dictAmpiezze)

#print("Type JsonCoordinte ",type(jsonCoordinates))
# Otteniamo le coordinate del triangolo col valore massimo, che sarebbe l'ggetto in posizione 1 dell'array features
coordinates = jsonCoordinates["features"][1]["geometry"]["coordinates"][0]
centroid = fc.getCntroide(coordinates)

centerPointTriangle=geojson.centerPointTriangle

centerPointTriangle["geometry"]["coordinates"].append(centroid[0][0])
centerPointTriangle["geometry"]["coordinates"].append(centroid[0][1])


cRetta0=centroid[0][0] #+0.000000000100
cRetta1=centroid[0][1]#+0.000000000100
maxRetta0=maxCentralina1[0]
maxRetta1=maxCentralina1[1]

rettaCentraleTraingolo=geojson.rettaCentraleTraingolo

rettaCentraleTraingolo["geometry"]["coordinates"][0].append(cRetta0)
rettaCentraleTraingolo["geometry"]["coordinates"][0].append(cRetta1)
rettaCentraleTraingolo["geometry"]["coordinates"][1].append(maxRetta0)
rettaCentraleTraingolo["geometry"]["coordinates"][1].append(maxRetta1)


#Retta che passa per la centralina col valore max di pm10,e anche per le altre 2 centraline max
nordToCmax1=geojson.ventoDefinitivo1
nordToCmax2=geojson.ventoDefinitivo2
nordToCmax3=geojson.ventoDefinitivo3

#Lat e lon dei due punti per la retta che passa per la centralina MAX1
point1LonCmax1=maxCentralina1[0]
point1LatCmax1=maxCentralina1[1]+ (rette.getDpLineNordToCmax1()/100000)
#point1LatCmax1=maxCentralina1[1]+ (dp/100000)
#print("Config valuepm10",rette.getDpLineNordToCmax1(), dp)
point2LonCmax1=maxCentralina1[0]
point2LatCmax1=maxCentralina1[1]


#Lat e lon dei due punti per la retta che passa per la centralina MAX2
point1LonCmax2=maxCentralina2[0]
point1LatCmax2=maxCentralina2[1]+0.010000000000
point2LonCmax2=maxCentralina2[0]
point2LatCmax2=maxCentralina2[1]

#Lat e lon dei due punti per la retta che passa per la centralina MAX3
point1LonCmax3=maxCentralina3[0]
point1LatCmax3=maxCentralina3[1]+0.010000000000
point2LonCmax3=maxCentralina3[0]
point2LatCmax3=maxCentralina3[1]

nordToCmax1["geometry"]["coordinates"][0].append(point1LonCmax1)
nordToCmax1["geometry"]["coordinates"][0].append(point1LatCmax1)
nordToCmax1["geometry"]["coordinates"][1].append(point2LonCmax1)
nordToCmax1["geometry"]["coordinates"][1].append(point2LatCmax1)


nordToCmax2["geometry"]["coordinates"][0].append(point1LonCmax2)
nordToCmax2["geometry"]["coordinates"][0].append(point1LatCmax2)
nordToCmax2["geometry"]["coordinates"][1].append(point2LonCmax2)
nordToCmax2["geometry"]["coordinates"][1].append(point2LatCmax2)


nordToCmax3["geometry"]["coordinates"][0].append(point1LonCmax3)
nordToCmax3["geometry"]["coordinates"][0].append(point1LatCmax3)
nordToCmax3["geometry"]["coordinates"][1].append(point2LonCmax3)
nordToCmax3["geometry"]["coordinates"][1].append(point2LatCmax3)

gradiVento=gv.getGradiVentoMaxCentraline(geojson=geovuoto,coordinates=maxCentralina1)
gradiVento2=gv.getGradiVentoMaxCentraline(geojson=geovuoto,coordinates=maxCentralina2)
gradiVento3=gv.getGradiVentoMaxCentraline(geojson=geovuoto,coordinates=maxCentralina3)
#print("gradi vendt 1,2,3 ",gradiVento,gradiVento2,gradiVento3)

#Retta inclinazione vento per Centralina max1
linea=LineString([(point1LonCmax1,point1LatCmax1),(point2LonCmax1,point2LatCmax1)]) #retta che dal nord passa  per la centralina max
lineInclinate=rotate(linea,-22.5,origin=maxCentralina1) #retta inclinata di  -gradiVento in senso orario

newCoord1=lineInclinate.coords.xy[0].tolist()
newCoord2=lineInclinate.coords.xy[1].tolist()


#newPolygon=(Point(maxCentralina1)).buffer(0.00100)
#newPolygon=(Point(maxCentralina1)).buffer( (config.valueMaxPm10/100000))
#newPolygon=(Point(maxCentralina1)).buffer((dp/100000))

#newPolygon=shapely.affinity.scale(newPolygon,xfact=0.9,yfact=0.6)
#print("Lenght newPolygon",newPolygon.length," lengt raggio ",linea.length)


#rette.aggiungiRette(linea,maxCentralina1,jsonCoordinates)
#Aggiunge le rette con le info delle medie orarie di ogni centralina

for key,item in infoCentraline.items():
    arrayCoords=[float(item["lon"]),float(item["lat"])]
    if str(key) in [config.nomeCentralina1,config.nomeCentralina2,config.nomeCentralina3]:
        rette.addLineWithMarker(maxCentralina=arrayCoords,jsonCoordinate=jsonCoordinates,name=str(key))

#rette.addLineWithMarker(maxCentralina=maxCentralina1,jsonCoordinate=jsonCoordinates)

#time.sleep(1000)
#Centro retta verticale che passa per cmax1
#newCoordsRettaCmax1=linea.coords.xy[0].tolist()
#newCoordsRettaCmax2=linea.coords.xy[1].tolist()
#centroRettaCmax1=(newCoordsRettaCmax1[0]+newCoordsRettaCmax1[1])/2
#centroRettaCmax2=(newCoordsRettaCmax2[0]+newCoordsRettaCmax2[1])/2



#Retta che dal nord passa per la centralina max pm10 inclinata di -gradiventi in senso orario
ventoInclinato=geojson.ventoInclinato

#ventoInclinato["geometry"]["coordinates"][0].append(newCoord1[0])
#ventoInclinato["geometry"]["coordinates"][0].append(newCoord2[0])
#ventoInclinato["geometry"]["coordinates"][1].append(newCoord1[1])
#ventoInclinato["geometry"]["coordinates"][1].append(newCoord2[1])


#Retta inclinazione vento per Centralina max2
#linea2=LineString([(point1LonCmax2,point1LatCmax2),(point2LonCmax2,point2LatCmax2)]) #retta che dal nord passa  per la centralina max
#lineInclinate2=rotate(linea2,-gradiVento2,origin=maxCentralina2) #retta inclinata di  -gradiVento in senso orario

#newCoord1Cmax2=lineInclinate2.coords.xy[0].tolist()
#newCoord2Cmax2=lineInclinate2.coords.xy[1].tolist()

#centroEllisseXCmax2=(newCoord1Cmax2[0]+newCoord1Cmax2[1])/2
#centroEllisseYCmax2=(newCoord2Cmax2[0]+newCoord2Cmax2[1])/2

#Retta che dal nord passa per la centralina max pm10 inclinata di -gradiventi in senso orario
#ventoInclinato2=geojson.ventoInclinato2

#ventoInclinato2["geometry"]["coordinates"][0].append(newCoord1Cmax2[0])
#ventoInclinato2["geometry"]["coordinates"][0].append(newCoord2Cmax2[0])
#ventoInclinato2["geometry"]["coordinates"][1].append(newCoord1Cmax2[1])
#ventoInclinato2["geometry"]["coordinates"][1].append(newCoord2Cmax2[1])

#Retta inclinazione vento per Centralina max3
#linea3=LineString([(point1LonCmax3,point1LatCmax3),(point2LonCmax3,point2LatCmax3)]) #retta che dal nord passa  per la centralina max
#lineInclinate3=rotate(linea3,-gradiVento3,origin=maxCentralina3) #retta inclinata di  -gradiVento in senso orario

#newCoord1Cmax3=lineInclinate3.coords.xy[0].tolist()
#newCoord2Cmax3=lineInclinate3.coords.xy[1].tolist()

#centroEllisseXCmax3=(newCoord1Cmax3[0]+newCoord1Cmax3[1])/2
#centroEllisseYCmax3=(newCoord2Cmax3[0]+newCoord2Cmax3[1])/2

#Retta che dal nord passa per la centralina max pm10 inclinata di -gradiventi in senso orario
#ventoInclinato3=geojson.ventoInclinato3

#ventoInclinato3["geometry"]["coordinates"][0].append(newCoord1Cmax3[0])
#ventoInclinato3["geometry"]["coordinates"][0].append(newCoord2Cmax3[0])
#ventoInclinato3["geometry"]["coordinates"][1].append(newCoord1Cmax3[1])
#ventoInclinato3["geometry"]["coordinates"][1].append(newCoord2Cmax3[1])


jsonCoordinates["features"].append(centerPointTriangle)
jsonCoordinates["features"].append(rettaCentraleTraingolo)
jsonCoordinates["features"].append(nordToCmax1)  #Nord to cmax1
jsonCoordinates["features"].append(nordToCmax2)
jsonCoordinates["features"].append(nordToCmax3)
#jsonCoordinates["features"].append(ventoInclinato)
#jsonCoordinates["features"].append(ventoInclinato2)
#jsonCoordinates["features"].append(ventoInclinato3)


linea1=[(newCoord1[0],newCoord2[0]),(newCoord1[1],newCoord2[1])]
line2=[(cRetta0,cRetta1) ,(maxRetta0,maxRetta1)]
gammaAngle=angoli.ang(lineA=linea1,lineB=line2)
#print("gammaAngle",gammaAngle)

for key in jsonCoordinates["features"]:
    try:
        if key["geometry"]["type"]=="Point":
            if maxCentralina1[0]==key["geometry"]["coordinates"][0] and maxCentralina1[1]==key["geometry"]["coordinates"][1]:
                key["properties"]["gamma_vento"]=gammaAngle
    except Exception as execption:
            pass
        
        
#Calcolo del dp(posizione della fonte)
#print("cmax ",config.valueMaxPm10)
"""
S=math.pow(10,3)
p=1.25*(math.pow(10,3))
sp=S*p
div=sp/config.valueMaxPm10
dp=int(math.sqrt((div)))
print("dp ",dp)
"""
#L'indice del punto col max pm10 va sommanto di 2 perchè nelle prime due posizionei ci sono i 2 triangoli
jsonCoordinates["features"][config.indexPointMaxPm10+2]["properties"].update({"dp":dp})
"""
semiAsseMaggiore=dp/2

vMax=max(config.v)
V=config.intensitaVentoCmax
#print("vmax  v ",vMax,V)
divisione=V/vMax
radice=math.sqrt(1-math.pow(divisione,2))
semiAsseMinore=semiAsseMaggiore*radice
#print("semiasseMaggior  e minore",semiAsseMaggiore,semiAsseMinore)
"""


fileOutput="output/"+config.data+".geojson"

with open(fileOutput, "w") as fp:
    json.dump(jsonCoordinates, fp)

dirVento=config.dizMediaGiornaliera[config.nomeCentralina1]["direzione_vento"]
print("La probabilità che la direzione del vento sia localizzata a ",dirVento," è del ",str(config.probDay),"%")




    

