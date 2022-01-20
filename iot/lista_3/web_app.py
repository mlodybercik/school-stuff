from flask import Flask, json, request
from json import JSONDecodeError

app = Flask(__name__)

memory = {}

@app.route("/async/other_test/<identifier>", methods=["POST", "GET"])
def post(identifier):
    if request.method == "POST":
        if request.data:
            try:
                memory[identifier] = json.loads(request.data.decode("utf-8"))
            except JSONDecodeError:
                memory[identifier] = request.data.decode("utf-8")
            return "", 200
    else:
        try:
            return str(memory[identifier])
        except KeyError:
            pass
    return "", 404

@app.route("/async/other_test/", methods=["GET"])
def get():
    return json.dumps(memory), 200

app.run(port=9999, debug=False, host="0.0.0.0")