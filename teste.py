import json
import requests

url = "https://docs.cloud.intranet.pags/v1/search/search_index.json"

search_data = requests.get(url=url).json()

convert_json = json.dumps(search_data)
print(search_data)
# print(convert_json)
