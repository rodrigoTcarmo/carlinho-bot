import json
import requests

url = "https://docs.cloud.intranet.pags/v1/search/search_index.json"

search_data = requests.get(url=url).json()

for d in search_data["docs"]:
    print(d)

# print(search_data.docs)
