import json

with open("./lista_zakupow.json") as file:
    zakupy = json.loads(file.read())

zakupy["produkty"].append("jajka")
zakupy["produkty"].append("mleko")

with open("./lista_zakupow.json", "w") as file:
    file.write(json.dumps(zakupy))