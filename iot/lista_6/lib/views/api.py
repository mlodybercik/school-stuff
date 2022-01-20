from quart import Blueprint, jsonify, abort, request

from lib.aggregators.aggregator import Aggregator
from ..aggregators import enum as aggregator_enum
from .. import aggregators
from . import bad_request, error, ok

api = Blueprint("api", __name__, url_prefix="/api/")


@api.route("/")
async def index():
    return ":)", 200

@api.route("/status")
async def status():
    return {"type": "aggregator",
            "status": {name: v.status() for name, v in aggregators.items()}}, 200

@api.route("/status/<string:topic>")
async def status_topic(topic):
    if topic in aggregators:
        return aggregators[topic].status()
    else:
        return abort(404)

@api.route("/register/<string:aggregator>", methods=["POST"])
async def create_new_aggregator(aggregator):
    # {"type": ... Any of the aggregator types,
    #  "time": ... int > 0}
    if aggregator in aggregators:
        return error("this aggregator already exists!")
    
    if (data := await request.json):
        if "type" in data and "time" in data:
            try:
                _type = aggregator_enum[data["type"]]
            except KeyError:
                return error("bad type")
            try:
                time = int(data["time"])
                assert time > 0
            except (ValueError, AssertionError):
                return error("bad value")
            
            aggregators[aggregator] = Aggregator(aggregator, _type, time)
            return ok()    
    return error("bad request")

@api.route("/register/", methods=["POST"])
async def register():
    if (data := await request.json):
        if "name" in data:
            return await create_new_aggregator(data["name"])
    return error("bad request")
    

@api.route("/change/<string:aggregator>", methods=["POST"])
async def change_aggregator(aggregator):
    if aggregator not in aggregators:
        return error("this aggregator doesnt exist!")
    if (data := await request.json):
        if "type" in data and "time" in data:
            try:
                _type = aggregator_enum[data["type"]]
            except KeyError:
                return error("bad type")
            try:
                time = int(data["time"])
                assert time > 0
            except (ValueError, AssertionError):
                return error("bad value")

            aggregators[aggregator].changeAggregator(_type)
            aggregators[aggregator].timeperiod = time

            return ok()
    return error("bad request")

@api.route("/change/", methods=["POST"])
async def change():
    if (data := await request.json):
        if "name" in data:
            return await change_aggregator(data["name"])
    return error("bad request")


@api.route("/remove/<string:aggregator>", methods=["POST"])
async def remove_aggregator(aggregator):
    if aggregator not in aggregators:
        return error(f"this aggregator doesnt exist! {aggregator}")
    del aggregators[aggregator]
    return ok()

@api.route("/remove/", methods=["POST"])
async def remove():
    if (data := await request.json):
        if "name" in data:
            return await remove_aggregator(data["name"])
    return error("bad request")