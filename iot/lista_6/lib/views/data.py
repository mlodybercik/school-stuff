from quart import Blueprint, jsonify, abort, request

from . import logger, missing, ok
logger = logger.getChild("data")

from .. import aggregators

data = Blueprint("data", __name__)

@data.route("/<string:topic>/", methods=["GET"])
async def index(topic):
    if topic in aggregators:
        return jsonify(aggregators[topic].getData()), 200
    else:
        return abort(404)


@data.route("/<string:topic>/<string:endpoint>", methods=["POST"])
async def post_data(topic: str, endpoint: str):
    if topic in aggregators:
        if (data := await request.json):
            aggregators[topic].receiveData(data["data"], endpoint)
            logger.info(f"Received data from on /{topic}/{endpoint}")
            return ok()
        elif (data := (await request.data).decode(request.charset)):
            aggregators[topic].receiveData(data, endpoint)
            return ok()

    return abort(400)