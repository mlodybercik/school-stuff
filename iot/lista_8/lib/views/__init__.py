from quart import jsonify
from .. import logger

logger = logger.getChild("views")

async def server_died(e):
    return "<img src='https://http.cat/500.jpg'>", 500

async def bad_request(e):
    return "<img src='https://http.cat/400.jpg'>", 400

async def missing(e):
    return "<img src='https://http.cat/404.jpg'>", 404

def error(error_string):
    return jsonify({"error": error_string}), 400

def ok():
    return jsonify({"status": "ok"}), 200


from .api import api
from .data import data


__all__ = ["api", "data", "server_died", "bad_request", "missing"]