

#Ritorna i gradi del vento della centralina più espostata al pm10
def getGradiVentoMaxCentraline(geojson:dict,coordinates:list):
    print("Gradi vento ")
    for key in geojson["features"]:
        try:
            if key["geometry"]["type"]=="Point":
                #print("coord",key["geometry"]["coordinates"])
                if coordinates[0]==key["geometry"]["coordinates"][0] and coordinates[1]==key["geometry"]["coordinates"][1]:
                  #print("sono uguali")
                  #print("id",key["properties"]["id"])
                  #print(key["properties"]["direzione_vento_gradi"])
                  return key["properties"]["direzione_vento_gradi"]
                else:
                  print("non uguali")
        except Exception as execption:
            pass