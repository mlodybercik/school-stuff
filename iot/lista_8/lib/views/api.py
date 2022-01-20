from quart import Blueprint, jsonify, abort, request, send_file

from ..aggregators import aggregator_enum
from ..aggregators.graph_logic import graph_enum
from .. import aggregator
from . import bad_request, error, ok

api = Blueprint("api", __name__, url_prefix="/api/")


@api.route("/")
async def index():
    return ":)", 200

@api.route("/status")
async def status():
    return {"type": "graphing-aggregator",
            "status": aggregator.status()}, 200

@api.route("/change/", methods=["POST"])
async def change_aggregator():
    if (data := await request.json):
        if "agg_type" in data and "time" in data and "graph_type" in data:
            try:
                agg_type = aggregator_enum[data["agg_type"]]
                graph_type = graph_enum[data["graph_type"]]
            except KeyError:
                return error("bad type")
            try:
                time = int(data["time"])
                assert time > 0
            except (ValueError, AssertionError):
                return error("bad value")

            aggregator.changeAggregator(agg_type)
            aggregator.timeperiod = time
            aggregator.graph = graph_type

            return ok()
    return error("bad request")

@api.route("/get_graph")
async def get_graph():
    if request.args:
        args = request.args
    elif (args := await request.json):
        pass
    else:
        args = {}
        
    image = aggregator.getGraph(**args)
    #TODO: i shouldnt hardcode the MIME type
    return await send_file(image, "image/svg+xml")