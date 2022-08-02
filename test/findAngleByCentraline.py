import json
with open("result_main3/centerPolygon.geojson","r") as file:
    geo=file.read()
    print(geo)
    print(type(geo))
geo=json.loads(geo)
array1=geo["features"][2]
#print(array1)
for key,item in array1.items():
        print(key)
        print(item)
        print("--------------\n")


def findAngle(geojson:dict):
    for key,item in geojson.items():
        print(key)
        print(item)
        print("--------------\n")
        pass