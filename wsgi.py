import logging

from urls import url_routes
from views import handler_404


logger = logging.getLogger(__name__)


def application(environ, start_response):
    url_route = url_routes.get(environ.get('PATH_INFO'), handler_404)
    return url_route(environ, start_response)