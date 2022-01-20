import urllib.request
import json

with urllib.request.urlopen("https://www.githubstatus.com/api/v2/status.json") as response:
    json_data = json.loads(response.read().decode("utf-8"))
    print(json_data)