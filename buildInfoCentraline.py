from numpy import inf
import requestInformation as ri
from shapely.geometry import LineString
import json
import angoli
import config
import maxIntensitaVento as miv
import hourlyAverages 
"""_summary_
Al geojson in input aggiunge gli oggetti che rappresentano i punti dei vertici con le relative properties
 """
def getGeojsonCentralineWithPoints(infoCentraline:dict,geovuoto:dict,dictAmpiezze:dict):
  print("into build ")  
  indexMaxPm10=0  
  for key,value in infoCentraline.items():
    dictInfoKey=ri.getInfo(key,config.data,config.data)
    #hourlyAverages.getInfo(key,config.data,config.data)
    #intensita_15giorni=miv.getMaxIntensitaVentoLastTwoWeek(key,config.data)
    if dictInfoKey is not None:
        if dictInfoKey["pm10"]== config.valueMaxPm10:
            config.nomeMaxCentralina=str(key)  #Inizalizza la variabile globale col nome della centralina che registra il valore massimo di pm10
            config.indexPointMaxPm10=indexMaxPm10
            config.intensitaVentoCmax=dictInfoKey["intensita_vento"]
            config.intensitaVentoGradiCmax=dictInfoKey["direzione_vento_gradi"]
        else:
            indexMaxPm10=indexMaxPm10+1
        config.v.append(float(dictInfoKey["intensita_vento"]))
        dictInfoKey["intensita_15_day"]=miv.getMaxIntensitaVentoLastTwoWeek(key,config.data)
        infoPoint={
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
        #geovuoto["features"].append(infoPoint)
        if key in dictAmpiezze:
            angle={"ampiezza_angolo":dictAmpiezze[key]}
            infoPoint["properties"].update(angle)
        geovuoto["features"].append(infoPoint)
    else:
        infoPoint={
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
        if key in dictAmpiezze:
            angle={"Ampizza angolo":dictAmpiezze[key]}
            infoPoint["properties"].update(angle)
        geovuoto["features"].append(infoPoint)
  return geovuoto
              

      

