
import json
import buildInfoCentraline as buildInfo

test={
  "type": "FeatureCollection",
  "features": [{
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
      "coordinates": [
        [
          [
              14.801567,
              40.828705
            ],
            [
              14.810876,
              40.821009
            ],
            [
              14.809813,
              40.828199
            ],
            [
              14.801567,
              40.828705
            ]
        ]
      ]
    }
  }, {
    "type": "Feature",
    "properties": {
        "stroke": "#C70039",
        "stroke-width": 3,
        "stroke-opacity": 1,
        "fill": "#FF0000",
        "fill-opacity": 0.5
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [
              14.809813,
              40.828199
            ],
            [
              14.810876,
              40.821009
            ],
            [
              14.819923,
              40.824999
            ],
            [
              14.809813,
              40.828199
            ]
        ]
      ]
    }
  }
  ]
}

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

jsonCoordinates=buildInfo.getGeojsonCentralineWithPoints(infoCentraline=infoCentraline,geovuoto=test)
with open("result_main3/multiPolygon1.geojson","w") as fp:
     json.dump(jsonCoordinates,fp)
