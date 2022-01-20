from flask import Flask, request

app = Flask(__name__)

curr_data = ""

@app.route("/cpu", methods=["GET", "POST"])
def cpu():
    global curr_data
    if request.method == "POST":
        curr_data = request.data.decode("utf-8")
        return "", 200
    else:
        return curr_data, 200


if __name__ == "__main__":
    app.run("127.0.0.1", 9999)