import json
from textwrap import indent
import triangulationModule as tm 
import geojson 

directory="coordinates/"
filename="giffoni.geojson"
locationFile=directory+""+filename
with open(locationFile,"r") as f:
    jsonCoordinates=json.load(f)
    
features=(jsonCoordinates["features"][0])
geometry=features["geometry"]
coordinates=geometry["coordinates"][0]

listTraingles=tm.traingulatePolygon(coordinates)

if listTraingles is not None:
    #print("Array non vuoto",type(listTraingles))
    geoJsonObject= {"type":"FeatureCollection","features":
                [
                    {
                        "type":"Feature","properties":
                            {"stroke":"#ff0000","stroke-width":2,"stroke-opacity":1,"fill":"#555555","fill-opacity":0.5},
                        "geometry":{"type":"Polygon","coordinates":listTraingles.tolist()}
                    }
                ]
            }

    #print(type(geoJsonObject))
    #print(geoJsonObject.__str__().replace("'", '"'))
    #outputfile=str(filename).replace("coordinates","result")
    #print("Output File",outputfile)
    outputfile="result/"+filename.split(".")[0] + "mod.geojson"
    #outputfile=filename.split(".")[0] + "mod.geojson"
    try:
        with open(outputfile,'w') as f:
            f.write(str(geoJsonObject.__str__().replace("'", '"')))
            #f.close()
    except Exception as ex:
        print(str(ex))
else:
    print("None")
