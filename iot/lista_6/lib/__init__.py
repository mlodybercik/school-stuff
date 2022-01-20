import logging
from quart import Quart
from typing import Dict

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from lib.aggregators import Aggregator
aggregators: Dict[str, Aggregator] = {}

def create_app() -> Quart:
    from .views import api, data, server_died, missing, bad_request
    app = Quart(__name__)

    app.register_blueprint(api)
    app.register_blueprint(data)
    app.register_error_handler(500, server_died)
    app.register_error_handler(404, missing)
    app.register_error_handler(400, bad_request)

    logger.info("creating app")
    return app