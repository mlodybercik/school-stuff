import logging
from typing import List
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

import ssl
import certifi

sslcontext = ssl.create_default_context(cafile=certifi.where())

from quart import Quart
from .service import Manager, Service

manager = Manager()

def create_app(services: List[Service]) -> Quart:
    from .views import controller, static

    for item in services:
        manager[item.name] = item
    
    app = Quart(__name__)

    app.register_blueprint(controller)
    app.register_blueprint(static)

    logger.info("creating app")
    return app

