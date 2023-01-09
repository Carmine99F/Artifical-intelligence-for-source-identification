from copy import copy
from distutils.command.config import config
from sys import intern
import centralineModule as cm
import json
import buildInfoCentraline as buildInfo
import triangulationModule as tm
import findCentroide as fc
import time
import angoli
import math
import shapely.affinity
from shapely.geometry import Point,Polygon
from shapely.geometry import LineString,MultiLineString
from shapely.affinity import rotate
from shapely.ops import triangulate
from sympy import Point as pt, Circle, Eq
import gradiVento as gv
from sympy import Line
import config
import geojson
import requests
import pyttsx3
import hourlyAverages as ha
import rette
#arrayCentraline = ['ITCAMMON134567', 'ITCAMMON234567',
#                   'ITCAMMON334567', 'ITCAMMON444567']
"""
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
"""
arrayCentraline = ['ITLOMBAS123456','ITLOMBAS234567', 'ITLOMBAS334567']

infoCentraline={}

for nameCentraline in arrayCentraline:
    re= requests.post("https://square.sensesquare.eu:5002/informazioni_centralina", data={"apikey": "WDBNX4IUF66C", "ID": nameCentraline})
    #print(re.text)
    infoCentraline[nameCentraline]={}
    infoCentraline[nameCentraline]['lat']= re.json()['result']['lat']
    infoCentraline[nameCentraline]['lon']= re.json()['result']['lon']
    
print(infoCentraline)


geovuoto=geojson.geovuoto
arrayPointTriangle=[]

maxCentralina1, maxCentralina2, maxCentralina3 = cm.getMaxCoordinates(arrayCentraline, infoCentraline)
print("maxC1",maxCentralina1)
print("maxC2",maxCentralina2)
print("maxC3",maxCentralina3)




#date le coordinate del trinagolo rosso , la funzione restituisce  un dizionario con le info relative agli angoli
dictAmpiezze= angoli.getAngle_sss(maxCentralina1, maxCentralina2, maxCentralina3, infoCentraline)




S=math.pow(10,3)
p=1.25*(math.pow(10,3))
sp=S*p
div=sp/config.valueMaxPm10
dp=int(math.sqrt((div)))

# Inseriamo l'intero poligono
for item in arrayCentraline:
    arraycoo = [infoCentraline[item]["lon"], infoCentraline[item]["lat"]]
    arrayPointTriangle.append(tuple(arraycoo))
    geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)
    
geovuoto["features"][0]['geometry']["coordinates"][0].append(geovuoto["features"][0]['geometry']["coordinates"][0][0])
arrayPointTriangle.append(arrayPointTriangle[0])
#print(arrayPointTriangle)
triangle=Polygon(arrayPointTriangle)
# Inseriamo il triangolo rosso
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina1)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina2)
geovuoto["features"][1]['geometry']["coordinates"][0].append(maxCentralina3)
geovuoto["features"][1]['geometry']["coordinates"][0].append(geovuoto["features"][1]['geometry']["coordinates"][0][0])

print("Max centraline 1",list(maxCentralina1))
# Aggiungiamo i punti  sui vertici del poligono
jsonCoordinates = buildInfo.getGeojsonCentralineWithPoints(infoCentraline=infoCentraline,
                                                           geovuoto=geovuoto, dictAmpiezze=dictAmpiezze)

print("Type JsonCoordinte ",type(jsonCoordinates))
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
print("Config valuepm10",rette.getDpLineNordToCmax1(), dp)
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
print("gradi vendt 1,2,3 ",gradiVento,gradiVento2,gradiVento3)

#Retta inclinazione vento per Centralina max1
linea=LineString([(point1LonCmax1,point1LatCmax1),(point2LonCmax1,point2LatCmax1)]) #retta che dal nord passa  per la centralina max
lineInclinate=rotate(linea,-22.5,origin=maxCentralina1) #retta inclinata di  -gradiVento in senso orario

newCoord1=lineInclinate.coords.xy[0].tolist()
newCoord2=lineInclinate.coords.xy[1].tolist()

centroEllisseX=(newCoord1[0]+newCoord1[1])/2
centroEllisseY=(newCoord2[0]+newCoord2[1])/2
"""
degressInclination=22.5
arrayNewPolygon=[]
for i in range(16):
    degressInclination=degressInclination+22.5
    lineInclinate=rotate(linea,degressInclination,origin=maxCentralina1)
    newCoord1=lineInclinate.coords.xy[0].tolist()
    newCoord2=lineInclinate.coords.xy[1].tolist()
    #print("newCoord1 ",newCoord1)
    #print("newCoord2 ",newCoord2)
    ventoInclinato = {
        "type": "Feature",
        "properties": {
            "stroke": "#FFFFFF",
            "stroke-width": 1,
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
    arrayNewPolygon.append((newCoord1[0],newCoord2[0]))
    #ventoInclinato["geometry"]["coordinates"][0].append(newCoord1[0])
    #ventoInclinato["geometry"]["coordinates"][0].append(newCoord2[0])
    #ventoInclinato["geometry"]["coordinates"][1].append(newCoord1[1])
    #ventoInclinato["geometry"]["coordinates"][1].append(newCoord2[1])
    #jsonCoordinates["features"].append(ventoInclinato)
"""
"""
newPolygon=Polygon(arrayNewPolygon)
newPolygon=shapely.affinity.scale(newPolygon,xfact=0.8,yfact=0.5)
newPolygon=newPolygon.buffer(0.000010000,resolution=16)
print("Nuovo poligono ",type(newPolygon)," area ",newPolygon.area )

"""
#newPolygon=(Point(maxCentralina1)).buffer(0.00100)
#newPolygon=(Point(maxCentralina1)).buffer( (config.valueMaxPm10/100000))
newPolygon=(Point(maxCentralina1)).buffer((dp/100000))

newPolygon=shapely.affinity.scale(newPolygon,xfact=0.9,yfact=0.6)
print("Lenght newPolygon",newPolygon.length," lengt raggio ",linea.length)


#rette.aggiungiRette(linea,maxCentralina1,jsonCoordinates)
#Aggiunge le rette con le info delle medie orarie di ogni centralina
for key,item in infoCentraline.items():
    print("Key ",key)
    print("item ",item)
    arrayCoords=[float(item["lon"]),float(item["lat"])]
    print(arrayCoords)
    rette.addLineWithMarker(maxCentralina=arrayCoords,jsonCoordinate=jsonCoordinates,name=str(key))

#rette.addLineWithMarker(maxCentralina=maxCentralina1,jsonCoordinate=jsonCoordinates)

#time.sleep(1000)
#Centro retta verticale che passa per cmax1
newCoordsRettaCmax1=linea.coords.xy[0].tolist()
newCoordsRettaCmax2=linea.coords.xy[1].tolist()
centroRettaCmax1=(newCoordsRettaCmax1[0]+newCoordsRettaCmax1[1])/2
centroRettaCmax2=(newCoordsRettaCmax2[0]+newCoordsRettaCmax2[1])/2



#Retta che dal nord passa per la centralina max pm10 inclinata di -gradiventi in senso orario
ventoInclinato=geojson.ventoInclinato

ventoInclinato["geometry"]["coordinates"][0].append(newCoord1[0])
ventoInclinato["geometry"]["coordinates"][0].append(newCoord2[0])
ventoInclinato["geometry"]["coordinates"][1].append(newCoord1[1])
ventoInclinato["geometry"]["coordinates"][1].append(newCoord2[1])


#Retta inclinazione vento per Centralina max2
linea2=LineString([(point1LonCmax2,point1LatCmax2),(point2LonCmax2,point2LatCmax2)]) #retta che dal nord passa  per la centralina max
lineInclinate2=rotate(linea2,-gradiVento2,origin=maxCentralina2) #retta inclinata di  -gradiVento in senso orario

newCoord1Cmax2=lineInclinate2.coords.xy[0].tolist()
newCoord2Cmax2=lineInclinate2.coords.xy[1].tolist()

centroEllisseXCmax2=(newCoord1Cmax2[0]+newCoord1Cmax2[1])/2
centroEllisseYCmax2=(newCoord2Cmax2[0]+newCoord2Cmax2[1])/2

#Retta che dal nord passa per la centralina max pm10 inclinata di -gradiventi in senso orario
ventoInclinato2=geojson.ventoInclinato2

ventoInclinato2["geometry"]["coordinates"][0].append(newCoord1Cmax2[0])
ventoInclinato2["geometry"]["coordinates"][0].append(newCoord2Cmax2[0])
ventoInclinato2["geometry"]["coordinates"][1].append(newCoord1Cmax2[1])
ventoInclinato2["geometry"]["coordinates"][1].append(newCoord2Cmax2[1])

#Retta inclinazione vento per Centralina max3
linea3=LineString([(point1LonCmax3,point1LatCmax3),(point2LonCmax3,point2LatCmax3)]) #retta che dal nord passa  per la centralina max
lineInclinate3=rotate(linea3,-gradiVento3,origin=maxCentralina3) #retta inclinata di  -gradiVento in senso orario

newCoord1Cmax3=lineInclinate3.coords.xy[0].tolist()
newCoord2Cmax3=lineInclinate3.coords.xy[1].tolist()

centroEllisseXCmax3=(newCoord1Cmax3[0]+newCoord1Cmax3[1])/2
centroEllisseYCmax3=(newCoord2Cmax3[0]+newCoord2Cmax3[1])/2

#Retta che dal nord passa per la centralina max pm10 inclinata di -gradiventi in senso orario
ventoInclinato3=geojson.ventoInclinato3

ventoInclinato3["geometry"]["coordinates"][0].append(newCoord1Cmax3[0])
ventoInclinato3["geometry"]["coordinates"][0].append(newCoord2Cmax3[0])
ventoInclinato3["geometry"]["coordinates"][1].append(newCoord1Cmax3[1])
ventoInclinato3["geometry"]["coordinates"][1].append(newCoord2Cmax3[1])


jsonCoordinates["features"].append(centerPointTriangle)
jsonCoordinates["features"].append(rettaCentraleTraingolo)
jsonCoordinates["features"].append(nordToCmax1)  #Nord to cmax1
#jsonCoordinates["features"].append(ventoCmax2)
#jsonCoordinates["features"].append(ventoCmax3)
#jsonCoordinates["features"].append(ventoInclinato)
#jsonCoordinates["features"].append(ventoInclinato2)
#jsonCoordinates["features"].append(ventoInclinato3)


linea1=[(newCoord1[0],newCoord2[0]),(newCoord1[1],newCoord2[1])]
line2=[(cRetta0,cRetta1) ,(maxRetta0,maxRetta1)]
gammaAngle=angoli.ang(lineA=linea1,lineB=line2)
print("gammaAngle",gammaAngle)

for key in jsonCoordinates["features"]:
    try:
        if key["geometry"]["type"]=="Point":
            #print("coord",key["geometry"]["coordinates"])
            if maxCentralina1[0]==key["geometry"]["coordinates"][0] and maxCentralina1[1]==key["geometry"]["coordinates"][1]:
                key["properties"]["gamma_vento"]=gammaAngle
            else:
                pass
                #print("non uguali")
    except Exception as execption:
            pass
        
        
#Calcolo del dp(posizione della fonte)
print("cmax ",config.valueMaxPm10)

S=math.pow(10,3)
p=1.25*(math.pow(10,3))
sp=S*p
div=sp/config.valueMaxPm10
dp=int(math.sqrt((div)))
print("dp ",dp)
#L'indice del punto col max pm10 va sommanto di 2 perchè nelle prime due posizionei ci sono i 2 triangoli
jsonCoordinates["features"][config.indexPointMaxPm10+2]["properties"].update({"dp":dp})

semiAsseMaggiore=dp/2

vMax=max(config.v)
V=config.intensitaVentoCmax
#print("vmax  v ",vMax,V)
divisione=V/vMax
radice=math.sqrt(1-math.pow(divisione,2))
semiAsseMinore=semiAsseMaggiore*radice
#print("semiasseMaggior  e minore",semiAsseMaggiore,semiAsseMinore)

#ELLISSE CMAX1
#circle = Point( centroEllisseX,centroEllisseY).buffer(0.000100)  # type(circle)=polygon
ellissi = Point(maxCentralina1[0],maxCentralina1[1]).buffer(0.000840000000,resolution=16,cap_style=1)  # type(circle)=polygon
#ellissi = LineString([(maxCentralina1[0],maxCentralina1[1]),(maxCentralina1[1]+0.000010,maxCentralina1[0]+0.000010)]).buffer(0.009,resolution=16,join_style=1) 
#ellissi = LineString([(0.2,0.1),(0.3,0.4)]).buffer(0.00100,resolution=100,join_style=1) 
#print("Type circle",type(circle))
#ellissi = shapely.affinity.scale(ellissi,20,20)
#ellissi = shapely.affinity.scale(circle,1,1)
#ellissi=shapely.affinity.rotate(ellissi,gradiVento,origin="centroid")

#print("Tipo ellissi ", type(ellissi))

#Ellisse CMAX1 Rotazione
circleRotate = Point(centroRettaCmax1,centroRettaCmax2).buffer(0.00012,resolution=100,cap_style=1)  # type(circle)=polygon
ellissiCmax1Rotate = shapely.affinity.scale(circleRotate,centroRettaCmax1,centroRettaCmax2)
ellissiCmax1Rotate=shapely.affinity.rotate(ellissiCmax1Rotate,-gradiVento,origin="centroid")
ellissiCmax1Rotate=shapely.affinity.rotate(ellissi,-270,origin=(centroRettaCmax1,centroRettaCmax2,0))

#ELLISSE CMAX2
circle2 = Point(centroEllisseXCmax2,centroEllisseYCmax2).buffer(0.00010000,resolution=8,cap_style=1)  # type(circle)=polygon
ellissi2 = shapely.affinity.scale(circle2,centroEllisseX,centroEllisseY,origin="centroid")
#ellissi2=Circle(pt(centroEllisseXCmax2,centroEllisseYCmax2),dp/2)
arrayLineString=[]
degressInclination=gradiVento
multiline=LineString()
arrayLine=[]
for i in range(12):
    if i>0:
        degressInclination=degressInclination+22.5
    newJsonLinestring=ventoDefinitivo1 = {
                "type": "Feature",
                "properties": {
                    "stroke": "#C70039",
                    "stroke-width": 4,
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
    linea=rotate(linea,-degressInclination,origin=maxCentralina1)
    #jsonCoordinates["features"].append(neJsonLinestring)
    newJsonLinestring["geometry"]["coordinates"][0].append(linea.coords[0][0])
    newJsonLinestring["geometry"]["coordinates"][1].append(linea.coords[0][1])
    newJsonLinestring["geometry"]["coordinates"][0].append(linea.coords[1][0])
    newJsonLinestring["geometry"]["coordinates"][1].append(linea.coords[1][1])
    #neJsonLinestring["geometry"]["coordinates"][0].append(newCoord2Cmax3[0])
    #jsonCoordinates["features"].append(neJsonLinestring)
newJsonLinestring=ventoDefinitivo1 = {
                "type": "Feature",
                "properties": {
                    "stroke": "#C70039",
                    "stroke-width": 4,
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
linea=rotate(linea,-degressInclination+220.5,origin=maxCentralina1)
    #jsonCoordinates["features"].append(neJsonLinestring)

newJsonLinestring["geometry"]["coordinates"][0].append(linea.coords[0][0])
newJsonLinestring["geometry"]["coordinates"][1].append(linea.coords[0][1])
newJsonLinestring["geometry"]["coordinates"][0].append(linea.coords[1][0]+84)
newJsonLinestring["geometry"]["coordinates"][1].append(linea.coords[1][1])

#jsonCoordinates["features"].append(neJsonLinestring)

#ellissi2=shapely.affinity.rotate(ellissi2,-gradiVento2,origin="centroid")

#ELLISSE CMAX3
circle3 = Point(centroEllisseXCmax3,centroEllisseYCmax3).buffer(0.00010,resolution=100,cap_style=1)  # type(circle)=polygon
ellissi3 = shapely.affinity.scale(circle3,centroEllisseXCmax3,centroEllisseYCmax3)
ellissi3 = shapely.affinity.scale(circle3,xfact=6.5,yfact=4.5)
ellissi3=shapely.affinity.rotate(ellissi3,-gradiVento3,origin="centroid")



eclipse=Polygon(ellissi)
#print(eclipse.exterior.coords)
listCordEllipse=list(eclipse.exterior.coords)
#print("Lista cordinate cerchio ",list(eclipse.exterior.coords))
eclipseRotate=Polygon(ellissiCmax1Rotate)
#print(eclipseRotate.exterior.coords)
listCordEllipseRotate=list(eclipseRotate.exterior.coords)


eclipse2=Polygon(ellissi2)
listCordEllipse2=list(eclipse2.exterior.coords)

eclipse3=Polygon(ellissi3)
listCordEllipse3=list(eclipse3.exterior.coords)

ellipse=geojson.eclipseJSON
ellipseRotate=geojson.eclipseJSONRotate
ellipse2=geojson.eclipseJSON2
ellipse3=geojson.eclipseJSON3
polygon=geojson.polygon

for i in range(len((listCordEllipse))):
    ellipse["geometry"]["coordinates"][0].append(list(listCordEllipse[i]))
for i in range(len((listCordEllipseRotate))):
    ellipseRotate["geometry"]["coordinates"][0].append(list(listCordEllipseRotate[i]))

for i in range(len((listCordEllipse2))):
    ellipse2["geometry"]["coordinates"][0].append(list(listCordEllipse2[i]))
for i in range(len((listCordEllipse3))):
    ellipse3["geometry"]["coordinates"][0].append(list(listCordEllipse3[i]))

listNewPolygon=list(newPolygon.exterior.coords)
for i in range(len(listNewPolygon)):
     polygon["geometry"]["coordinates"][0].append(list(listNewPolygon[i]))
    



#jsonCoordinates["features"].append(ellipse)
#jsonCoordinates["features"].append(ellipseRotate)
#jsonCoordinates["features"].append(ellipse2)
#jsonCoordinates["features"].append(ellipse3)
#jsonCoordinates["features"].append(polygon)
fileOutput="resultFinal2/"+config.data+".geojson"

with open(fileOutput, "w") as fp:
    json.dump(jsonCoordinates, fp)


pointEllipse=Point(eclipse.exterior.coords)


print("Are Intersezione",newPolygon.intersection(triangle).area)
polygonIntersection=Polygon(newPolygon.intersection(triangle))
reportArea=polygonIntersection.area/eclipse.area

intern=None
print(type(reportArea))
if reportArea < 0.5:
    print("Report area < 0.5 ",reportArea)
    intern="Esterno"
else:
    intern="Interno"
    print("Report area  > 0.5",reportArea)

coordIntersection=list(polygonIntersection.exterior.coords)
pInter=geojson.Intersection
for i in range(len((coordIntersection))):
    pInter["geometry"]["coordinates"][0].append(list(coordIntersection[i]))
    
#jsonCoordinates["features"].append(pInter)
with open(fileOutput, "w") as fp:
    json.dump(jsonCoordinates, fp)

if gradiVento>=0 and gradiVento<45:
    text="L'inquinamento probabilmente proviene è {} e proviene da Nord con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=45 and gradiVento<90:
    text="L'inquinamento probabilmente  è {} e proviene da Nord-Est con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=90 and gradiVento<135:
    print("Est")
    text="L'inquinamento probabilmente  è {} e proviene da EST con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=135 and gradiVento<180:
    print("Sud-Est")
    text="L'inquinamento probabilmente  è {} e proviene da Sud-Est con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=180 and gradiVento<225:
    print("Sud")
    text="L'inquinamento probabilmente  è {} e proviene da Sud con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=225 and gradiVento<270:
    print("Sud-Ovest")
    text="L'inquinamento probabilmente  è {} e proviene da Sud-Ovest con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=270 and gradiVento<315:
    text="L'inquinamento probabilmente  è {} e proviene da Ovest con una distanza massima di {}metri quadrati".format(intern,dp)
if gradiVento>=315:
    text="L'inquinamento probabilmente  è {} e proviene da Nord-Ovest con una distanza massima di {}metri quadrati".format(intern,dp)
print(text)

#ha.getInfo(config.nomeMaxCentralina,"2022-10-24","2022-10-24")

engine=pyttsx3.init()
engine.setProperty('rate',130)
voice=engine.getProperty('voices')
engine.setProperty('voice',voice[0].id)
engine.say(text=text)
#engine.runAndWait()