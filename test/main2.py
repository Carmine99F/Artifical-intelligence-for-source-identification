import json
import geojson
import centralineModule as centraline
import maxTriangleByCentraline as mtbc
import buildInfoCentraline as buildInfo
import triangulationModule as tm

arrayCentraline = ['ITCAMMON134567', 'ITCAMMON234567',
                   'ITCAMMON334567', 'ITCAMMON444567']
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
geovuoto = {
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

for item in arrayCentraline:
    print(item)
    # ci prendiamo lat e lon dal backend per ogni sensore
    arraycoo = [infoCentraline[item]["lon"], infoCentraline[item]["lat"]]
    geovuoto["features"][0]['geometry']["coordinates"][0].append(arraycoo)

geovuoto["features"][0]['geometry']["coordinates"][0].append(
    geovuoto["features"][0]['geometry']["coordinates"][0][0])

directory = "coordinates/"
filename = "ProvaMax.geojson"
locationFile = directory+""+filename

jsonCoordinates = buildInfo.getGeojsonCentralineWithPoints(
    infoCentraline=infoCentraline, geovuoto=geovuoto)
with open("testPoint.geojson", "w") as fp:
    json.dump(jsonCoordinates, fp)

features = (jsonCoordinates["features"][0])
geometry = features["geometry"]
coordinates = geometry["coordinates"][0]

maxCentralina1, maxCentralina2, maxCentralina3 = centraline.getMaxCoordinates(
    arrayCentraline, infoCentraline)
if maxCentralina1 is not None and maxCentralina2 is not None and maxCentralina3 is not None:
    listTraingles = tm.traingulatePolygon(coordinates)
    triangleMaxPM10 = mtbc.getMaxTraingle(
        listTraingles, maxCentralina1, maxCentralina2, maxCentralina3)
    if listTraingles is not None:
        # trianglesGeojson["features"][0]["geometry"]["coordinates"].append(listTraingles.tolist())
        trianglesGeojson = {
            "type": "FeatureCollection",
            "features": [
                    {
                        "type": "Feature",
                        "properties": {
                                "stroke": "#C70039",
                                "stroke-width": 2,
                                "stroke-opacity": 1,
                                "fill": "#00FF00",
                                "fill-opacity": 0.5
                        },
                        "geometry": {
                            "type": "Polygon",
                                    "coordinates": listTraingles.tolist()
                        }
                    }
            ]
        }
        print(json.dumps(trianglesGeojson, indent=4))
    if triangleMaxPM10 is not None:
        # triangleMaxPM10Geojson["features"][0]["geometry"]["coordinates"].append(triangleMaxPM10.tolist)
        triangleMaxPM10Geojson = {
            "type": "FeatureCollection",
            "features": [
                    {
                        "type": "Feature",
                        "properties": {
                                "stroke": "#C70039",
                                "stroke-width": 2,
                                "stroke-opacity": 1,
                                "fill": "#FF0000",
                                "fill-opacity": 0.5
                        },
                        "geometry": {
                            "type": "Polygon",
                                    "coordinates": triangleMaxPM10.tolist()
                        }
                    }
            ]
        }
    outputfile1 = "result1/"+filename.split(".")[0] + "mod.geojson"
    outputfile2 = "result1/" + \
        filename.split(".")[0] + "modMaxCentraline.geojson"
    with open(outputfile1, 'w') as f:
        f.write(str(trianglesGeojson.__str__().replace("'", '"')))
    with open(outputfile2, 'w') as f:
        f.write(str(triangleMaxPM10Geojson.__str__().replace("'", '"')))
else:
    print("Alemento una delle 3 centraline vale None")
