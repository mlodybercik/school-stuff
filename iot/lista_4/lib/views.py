from quart import Blueprint, jsonify, request
from lib.getter import GettableDiskData, GettableWebData
from lib.sender import SenderHTTP, SenderMQTT
from . import manager

api = Blueprint("api", __name__, url_prefix="/api/")

@api.app_errorhandler(500)
async def server_died(e):
    return "<img src='https://http.cat/500.jpg'>"

@api.app_errorhandler(400)
async def bad_request(e):
    return "<img src='https://http.cat/400.jpg'>"

@api.app_errorhandler(404)
async def missing(e):
    return "<img src='https://http.cat/404.jpg'>"


def error(error_string="this service doesnt exist"):
    return jsonify({"error": error_string}), 400

def ok():
    return jsonify({"status": "ok"}), 200

@api.route("/status")
async def get_status():
    return jsonify(manager.status())

@api.route("/toggle_pause", methods=["POST", "GET"])
async def try_pause():
    try:
        if manager.instance.running:
            await manager.instance.exit()
        else:
            await manager.instance.start()
        return jsonify({"status": manager.instance.running})
    except KeyError:
        return error()

@api.route("/set_interval/<int:time>", methods=["POST", "GET"])
async def set_interval(time):
    try:
        manager.instance.period = time
        return ok()
    except KeyError:
        return error()

@api.route("/change_getter", methods=["POST", "GET"])
async def change_getter():
    if request.method == "GET":
        return jsonify({"type": "HTTP or file",
                        "url": "http://example.com",
                        "json": "bool: optional",
                        "path": "path to file on disk or path to given json resource"}), 400
        
    if request.method == "POST":
        if (json := await request.get_json()):
            try:
                type = json["type"]
                if "url" in json:
                    url = json["url"]
                else:
                    url = None
                path = json["path"]
                if "json" in json:
                    is_json = json["json"]
                else:
                    is_json = False
            except KeyError:
                return error("malformed json")
            
            if type == "HTTP":
                new = GettableWebData(url, path, is_json)
            elif type == "file":
                new = GettableDiskData(path)
            else:
                return error("weird type")

            try:
                if manager.instance.running:
                    await manager.instance.exit()
                    manager.instance.getter = new
                    await manager.instance.start()
                else:
                    manager.instance.getter = new
                return ok()
            except KeyError:
                return error()
            
    return error("weird request")


@api.route("/change_sender", methods=["GET", "POST"])
async def change_sender():
    if request.method == "GET":
        return jsonify({"address": "addres of endpoint, can be http[s]://... or mqtt[s]://...",
                        "topic": "topic for mqtt or endpoint of http"}), 400

    if request.method == "POST":
        if (json := await request.get_json()):
            try:
                address: str
                address = json["address"]
                topic = json["topic"]
            except KeyError:
                return error("malformed json")
            
            if address.startswith("http"):
                new = SenderHTTP(address, topic)
            elif address.startswith("mqtt"):
                new = SenderMQTT(address, topic)
            else:
                return error("weird type")

            try:
                if manager.instance.running:
                    await manager.instance.exit()
                    manager.instance.sender = new
                    await manager.instance.start()
                else:
                    manager.instance.sender = new
                return ok()
            except KeyError:
                return error()
    return error("weird request")
