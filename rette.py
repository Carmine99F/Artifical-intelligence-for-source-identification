from shapely.geometry import LineString
from shapely.affinity import rotate
import config
import hourlyAverages as ha
import json
import math
import calcoloProbabilità as cp

def getColorMarker(pm10):
    color=""
    if pm10<10:
        color="#00FF00"
    if pm10==10:
        color="#ADFF2F"
    if pm10> 10 and pm10<20:
        color="#F7FF76"
    if pm10==20:
        color="#EEFE00"
    if pm10>20 and pm10<30:
        color="#FFC52B"
    if pm10==30:
        color="#F49800"      
    if pm10>30 and pm10<50:
        color="#D66500"
    if pm10==50:
        color="#FC0400"
    if pm10>50:
        color="#C70300"
    return color 

def getHourlyProability(orario):
    dizHourly1:dict=config.dizMediaOraria[config.nomeCentralina1]
    dizHourly2:dict=config.dizMediaOraria[config.nomeCentralina2]
    dizHourly3:dict=config.dizMediaOraria[config.nomeCentralina3]
    if orario in dizHourly1.keys()  and orario in dizHourly2.keys() and orario in dizHourly3.keys():
        direzioneC1=config.dizMediaOraria[config.nomeCentralina1][orario]["direzione"]
        direzioneC2=config.dizMediaOraria[config.nomeCentralina2][orario]["direzione"]
        direzioneC3=config.dizMediaOraria[config.nomeCentralina3][orario]["direzione"]
        prob=cp.getRange(dirVentoC1=float(direzioneC1),dirVentoC2=float(direzioneC2),dirVentoC3=float(direzioneC3))
    #print("prob  ", prob)
        return prob
    return 0
    #print(direzioneC1,direzioneC2,direzioneC3)

#getHourlyProability("10:00")
"""_summary_
    La funziona getInfo retituisce un dizionario con le info relative la media oraria della centralina cmax1
    in arrayDizionario vengono inseriti tutti i valori delle direzioni del vento
    se il numero della retta è presente nell'arrayDirezioni 

    Args:
        idLine (int): numero di retta
        jsonCoordinate (dict): geojson

    Returns:
        list: InfoPoint è un dizionario con le informazioni relative al marker, dp
"""
def getMarker(idLine:int,dictSensor: dict)->list:
   
    arrayDirezioni=[] #è un array che contiene tutti i valori delle direzioni del vento
    for key,item in dictSensor.items():
        arrayDirezioni.append(round(float(item["direzione"])))
        
    infoPoint={
            "type": "Feature",
            "properties": {
                "marker-color":"",
            },            
        "geometry": {
            "type": "Point",
            "coordinates": [                
                ]
            }
        }
    if idLine in arrayDirezioni:
        arrayPm10=[]
        intensitaVento=0
        #print("All keys ",json.dumps(dictSensor,indent=2))
        for key,item in dictSensor.items():   #dictSensore = {orario:{pm:"", direzione="",dp}}
            direzione=(round(float(item["direzione"])))
           #print("key ",key)
            probabilitaOraria:float=getHourlyProability(key)
            item["ph"]=probabilitaOraria
            if idLine == direzione:
                infoPoint["properties"].update({str(key):str(item)})
                arrayPm10.append(float(item["pm10"]))  # l'array di dp serve per il dp
                
        codeColor=getColorMarker(max(arrayPm10))
        dp=ha.getDP(max(arrayPm10))
        #cs=getConcentrazioneSorgente(intensitaVento,orario,dp)
        infoPoint["properties"].update({"marker-color":str(codeColor)})
        return infoPoint,dp
    return None,None

"""
    Questa funzione aggiunge alla centralina identificata dal parametro name le rette e i marker 
"""
def addLineWithMarker(maxCentralina:list,jsonCoordinate:dict,name:str):
    degressInclination=0
     #Dizionario relativo alla centralina name che contine le infomrmazioni relative  a ogni ora 
    dictSensor=config.dizMediaOraria[name]
    for i in range(16):
        degressInclination=degressInclination+22.5
        infoPoint,dp=getMarker(idLine= int(i+1),dictSensor=dictSensor)
       
        if infoPoint is not None and dp is not None:
            point1LonCmax1=maxCentralina[0]
            point1LatCmax1=maxCentralina[1]+((dp/100000))
            point2LonCmax1=maxCentralina[0]
            point2LatCmax1=maxCentralina[1]
            linea=LineString([(point1LonCmax1,point1LatCmax1),(point2LonCmax1,point2LatCmax1)]) #retta che dal nord passa  per la centralina max
            lineInclination=rotate(linea,-degressInclination,origin=maxCentralina)
            newCoord1=lineInclination.coords.xy[0].tolist()
            newCoord2=lineInclination.coords.xy[1].tolist()
            lineJson = {
                "type": "Feature",
                "properties": {
                    "stroke": "#1AA1FF",
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
            lineJson["geometry"]["coordinates"][0].append(newCoord1[0])
            lineJson["geometry"]["coordinates"][0].append(newCoord2[0])
            lineJson["geometry"]["coordinates"][1].append(newCoord1[1])
            lineJson["geometry"]["coordinates"][1].append(newCoord2[1])

            infoPoint["geometry"]["coordinates"].append(newCoord1[0])
            infoPoint["geometry"]["coordinates"].append(newCoord2[0])

            jsonCoordinate["features"].append(lineJson)
            jsonCoordinate["features"].append(infoPoint)

        
        
    """
    dp per la media giornaliera
    """
def getDpLineNordToCmax1():
    #dictSensor=ha.getInfo(nameCentralina=config.nomeMaxCentralina,data1=config.data,data2=config.data)
    dictSensor=config.dizMediaOraria[config.nomeMaxCentralina]
    #print("stampa")
    #print(dictSensor)
    arrayPm10=[]
    for key,item in dictSensor.items():
        arrayPm10.append(float(item["pm10"]))
    dp=ha.getDP(max(arrayPm10))
    return dp
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
