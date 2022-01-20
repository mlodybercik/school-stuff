import logging
logger = logging.getLogger('filter')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from quart import Quart

from lib.manager import Manager

manager = Manager()

def create_app() -> Quart:
    from .views import api
    app = Quart(__name__)

    app.register_blueprint(api)

    logger.info("creating app")
    return app
