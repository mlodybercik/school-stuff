from requests import get
import json

request = get("https://api.github.com/users/hadley/orgs")

if request.status_code == 200:
    data = json.loads(request.text)

data = sorted(data, key=lambda a: a["login"])

with open("random_json_data.json", "w") as file:
    file.write(json.dumps(data))