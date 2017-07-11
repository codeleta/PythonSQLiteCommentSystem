import logging.config

from wsgiref.simple_server import make_server

import settings
from wsgi import application

logging.config.dictConfig(settings.LOGGING_CONF)
logger = logging.getLogger("runserver")


def run_handle_request():
    server = make_server(settings.HOST, settings.PORT, application)
    logger.info('handle request started on {}:{}'.format(settings.HOST, settings.PORT))
    server.handle_request()


def run_server():
    server = make_server(settings.HOST, settings.PORT, application)
    logger.info('server started on {}:{}'.format(settings.HOST, settings.PORT))
    server.serve_forever()


if __name__ == "__main__":
    run_server()