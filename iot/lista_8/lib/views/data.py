from quart import Blueprint, jsonify, abort, request

from . import logger, missing, ok
logger = logger.getChild("data")

from .. import aggregator

data = Blueprint("data", __name__)

@data.route("/", methods=["GET"])
async def index():
    return jsonify(aggregator.getData()), 200


@data.route("/<string:endpoint>", methods=["POST"])
async def post_data(endpoint: str):
    if (data := await request.json):
        aggregator.receiveData(data["data"], endpoint)
        logger.info(f"Received data from on /{endpoint}")
        return ok()
    elif (data := (await request.data).decode(request.charset)):
        aggregator.receiveData(data, endpoint)
        logger.info(f"Received data from on /{endpoint}")
        return ok()
    else:
        return abort(400)
