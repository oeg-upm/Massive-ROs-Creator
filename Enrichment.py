import requests
import json
openAireURL = "https://api.openaire.eu/search/publications"

payload = {
        'doi': "10.5194/esd-10-569-2019",
        'format': "json",
        'size':100
   }
response=requests.get(openAireURL, params=payload)
f = open("Massive-ROs-Creator\Enrichment.json", "w")
f.write(json.dumps(response.json(), indent=4, sort_keys=True))
f.close()

print(response.json())