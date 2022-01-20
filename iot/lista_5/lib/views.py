import asyncio
from logging import Filter
from quart import Blueprint, json, jsonify, request, render_template, send_file, send_from_directory, redirect
from .service import Generator, Aggregator, FilterGenerator, GraphingAggregator
from werkzeug.exceptions import NotFound
from io import BytesIO

from .views_templates import *

from lib.service import Service
from . import manager

static = Blueprint("static", __name__, url_prefix="/static/")
@static.route("/js/<path:path>")
async def serve_js(path):
    try:
        return await send_from_directory("lib/static/js/", file_name=path)
    except NotFound as e:
        return await missing(e)
        
controller = Blueprint("controller", __name__)

@controller.app_errorhandler(500)
async def server_died(e):
    return "<img src='https://http.cat/500.jpg'>", 500

@controller.app_errorhandler(400)
async def bad_request(e):
    return "<img src='https://http.cat/400.jpg'>", 400

@controller.app_errorhandler(404)
async def missing(e):
    return "<img src='https://http.cat/404.jpg'>", 404

def error(error_string: str):
    return jsonify({"error": error_string}), 400

def ok():
    return jsonify({"status": "ok"}), 200

async def get_status(name):
    res = await manager[name].get_status()
    return (manager[name], res)

@controller.route("/")
async def index():
    # TODO: add possibility of serivce being paused, color-danger or sth.
    online = await asyncio.gather(*[get_status(m) for m in manager])
    return await render_template("index.jinja", manager=online)

@controller.route("/add", methods=["GET", "POST"])
async def add():
    if request.method == "GET":
        return await render_template("add.jinja")
    else:
        if (data := await request.json):
            try:
                manager[data["name"]] = Service(data["name"], data["address"])
                return ok()
            except KeyError:
                return error()
    return error()

@controller.route("/manage/<string:name>", methods=["GET", "POST"])
async def manage(name):
    try:
        service = manager[name]
    except KeyError as e:
        return await missing(e)
    
    if request.method == "GET":
        if (data := await service.get_status()):
            if data["type"] == "aggregator":
                #* im so fucking bored of doing this, gonna do this in a pretty weird way
                AGGREGATOR_REMOVE[0][-1] = list(data["status"].keys())
                AGGREGATOR_CHANGE[0][-1] = AGGREGATOR_REMOVE[0][-1]
            return await render_template("manage.jinja", 
                         service=service,
                         data=data,
                         forms={"GENERATOR_GETTER": GENERATOR_GETTER,
                                "GENERATOR_SENDER": GENERATOR_SENDER,
                                "AGGREGATOR_ADD": AGGREGATOR_ADD,
                                "AGGREGATOR_REMOVE": AGGREGATOR_REMOVE,
                                "AGGREGATOR_CHANGE": AGGREGATOR_CHANGE,
                                "FILTER_CHANGE": FILTER_CHANGE,
                                "FILTER_SENDER": FILTER_SENDER,
                                "FILTER_GETTER": FILTER_GETTER,
                                "AGGREGATOR_GRAPH_CHANGE": AGGREGATOR_GRAPH_CHANGE})
    else:
        if (data := await request.json):
            if data["type"] == "generator":
                if data["action"] == "change_sender":
                    ret = await Generator.handle_change_sender(service, data["form"])
                elif data["action"] == "change_getter":
                    ret = await Generator.handle_change_getter(service, data["form"])
                elif data["action"] == "toggle_pause":
                    ret = await Generator.handle_toggle_pause(service, data["form"])
                else:
                    return error("unknown action")
            elif data["type"] == "aggregator":
                if data["action"] == "add":
                    ret = await Aggregator.handle_add_aggregator(service, data["form"])
                elif data["action"] == "change":
                    ret = await Aggregator.handle_change_aggregator(service, data["form"])
                elif data["action"] == "remove":
                    ret = await Aggregator.handle_remove_aggregator(service, data["form"])
                else:
                    return error("unknown action")

            elif data["type"] == "generator-filter":
                if data["action"] == "toggle_pause":
                    ret = await FilterGenerator.handle_toggle_pause(service, data["form"])
                elif data["action"] == "change_sender":
                    ret = await FilterGenerator.handle_change_sender(service, data["form"])
                elif data["action"] == "change_getter":
                    ret = await FilterGenerator.handle_change_getter(service, data["form"])
                elif data["action"] == "change_filter":
                    ret = await FilterGenerator.handle_change_filter(service, data["form"])
                else:
                    return error("unknown action")
            elif data["type"] == "graphing-aggregator":
                if data["action"] == "change":
                    ret = await GraphingAggregator.handle_change(service, data["form"])
                else:
                    return error("unknown action")
    
            if ret:
                return ok()

        return error("json data missing")
    return redirect("/")
        
@controller.route("/manage/<string:name>/graph", methods=["GET", "POST"])
async def get_graph(name):
    try:
        service = manager[name]
    except KeyError as e:
        return await missing(e)

    if (image := await service.get("/api/get_graph", await request.json)):
        return await send_file(BytesIO(image), "image/svg+xml"), 200
    else:
        return error("bad request")
