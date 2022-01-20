from quart import Blueprint, jsonify, request
from lib.logic.filter import Filter
from lib.network.getter import GettableWebData
from lib.network.sender import SenderHTTP
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

@api.route("/set_interval/<int:time>")
async def set_interval(time):
    manager.instance.period = time
    return ok()

@api.route("/change_getter", methods=["POST", "GET"])
async def change_getter():
    if request.method == "GET":
        return jsonify({"url": "http://example.com"}), 400
        
    if request.method == "POST":
        if (json := await request.get_json()):
            try:
                if "url" in json:
                    url = json["url"]
            except KeyError:
                return error("malformed json")
            
            new = GettableWebData(url)
            

            try:
                if manager.instance.running:
                    await manager.instance.exit()
                    manager.instance.getter = new
                    await manager.instance.start()
                else:
                    manager.instance.getter = new
                return ok()
            except KeyError:
                return error("something wrong with manager???")
            
    return error("weird request")

@api.route("/change_sender", methods=["GET", "POST"])
async def change_sender():
    if request.method == "GET":
        return jsonify({"address": "addres of endpoint, can be http[s]://...",
                        "topic": "endpoint of http"}), 400

    if request.method == "POST":
        if (json := await request.get_json()):
            try:
                address = json["address"]
                topic = json["topic"]
            except KeyError:
                return error("malformed json")
            
            if address.startswith("http"):
                new = SenderHTTP(address, topic)
            else:
                return error("weird url")

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

@api.route("/change_filter", methods=["GET", "POST"])
async def change_filter():
    if request.method == "GET":
        return jsonify({"paths": ["list of paths to object", "data amount 'group 1' d"],
                        "soft": "true or false, whether should fail if path doesnt exist"}), 400

    if request.method == "POST":
        if (json := await request.get_json()):
            try:
                paths = json["paths"]
                soft = json["soft"]
            except KeyError:
                return error("malformed json")
            
            if isinstance(paths, list) and isinstance(soft, bool):
                manager.instance.filter = Filter(paths, soft)
                return ok()
                
    return error("weird request")