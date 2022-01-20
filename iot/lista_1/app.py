from flask import Flask, request
from typing import List
from dataclasses import dataclass

app = Flask(__name__)

memory = {}

@dataclass(init=False)
class TextContent:
    text: List[str]
    amount_of_lines: int

    def __init__(self, text: str):
        self.text = text.split("\n")
        self.amount_of_lines = len(self.text)

@app.route("/<name>", methods=["POST"])
def send_file(name):
    # if file in post
    if 'file' in request.files:
        # if file given check type and save it in memory
        if request.files['file'].filename.endswith(".txt"):
            text = request.files['file'].read().decode("utf-8")
            content = TextContent(text)
            memory[name] = content
            return name, 200
    return "No file given or bad extension", 404

@app.route("/<name>", methods=["GET"])
def get_file(name):
    if "linia" in request.args:
        try:
            line = int(request.args["linia"])
        except ValueError:
            line = -1
    else:
        line = -1
    if name in memory:
        if line == -1:
            return "\n".join(memory[name].text), 200
        try:
            return memory[name].text[line]
        except IndexError:
            pass
        return "\n".join(memory[name].text), 200
    else:
        return "name not in memory", 404

app.run("127.0.0.1", 5000, True)