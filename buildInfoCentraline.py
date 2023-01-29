import requestInformation as ri
#from shapely.geometry import LineString
import json
import angoli
import config
import hourlyAverages 

"""_summary_
Al geojson in input aggiunge gli oggetti(marker) che rappresentano i punti dei vertici con le relative properties
 """
def getGeojsonCentralineWithPoints(infoCentraline:dict,geovuoto:dict,dictAmpiezze:dict):
  #print("into build ")  
  indexMaxPm10=0  
  for key,value in infoCentraline.items():
    #dictInfoKey=ri.getInfo(key,config.data,config.data)
    dictInfoKey=config.dizMediaGiornaliera[key]
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
        #dictInfoKey["intensita_15_day"]=miv.getMaxIntensitaVentoLastTwoWeek(key,config.data)
        #dictInfoKey["intensita_15_day"]=ri.getIntensitaVento(key,config.data,config.data)
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
              

      
def getGeojsonCentralineWithPoints2(infoCentraline:dict,geovuoto:dict,dictAmpiezze:dict):  
  indexMaxPm10=0
  dictInfoKey:dict=config.dizMediaGiornaliera
  #print("Diz",json.dumps( dictInfoKey,indent=3))  
  for key,value in dictInfoKey.copy().items():
    print("Chiave attuale ",key)
    if dictInfoKey is not None:
        if dictInfoKey[key]["pm10"]== config.valueMaxPm10:
            config.nomeMaxCentralina=str(key)  #Inizalizza la variabile globale col nome della centralina che registra il valore massimo di pm10
            config.indexPointMaxPm10=indexMaxPm10
            print("Chiavi per ", key, dictInfoKey[key].keys())
            if "intensita_vento" in dictInfoKey[key].keys():
                config.intensitaVentoCmax=dictInfoKey[key]["intensita_vento"]
            config.intensitaVentoGradiCmax=dictInfoKey[key]["direzione_vento_gradi"]
        else:
            indexMaxPm10=indexMaxPm10+1
        if "intensita_vento" in dictInfoKey[key].keys():
            config.v.append(float(dictInfoKey[key]["intensita_vento"]))
        #dictInfoKey[key]["intensita_15_day"]=ri.getIntensitaVento(key,config.data,config.data)
        infoPoint={
            "type": "Feature",
            "properties": dictInfoKey[key],
            "geometry": {
                "type": "Point",
                "coordinates": [
                    value["lon"],
                    value["lat"]
                    ]
                }
            }
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
              

      



