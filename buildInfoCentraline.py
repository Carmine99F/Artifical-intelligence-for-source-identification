from numpy import inf
import requestInformation as ri
from shapely.geometry import LineString
import json
import angoli

"""_summary_
Al geojson in input aggiunge gli oggetti che rappresentano i punti dei vertici con le relative properties
 """
def getGeojsonCentralineWithPoints(infoCentraline:dict,geovuoto:dict,dictAmpiezze:dict):
  for key,value in infoCentraline.items():
    dictInfoKey=ri.getInfo(key)
    if dictInfoKey is not None:
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
              

      

