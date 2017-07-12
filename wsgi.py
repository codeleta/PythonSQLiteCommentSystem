import logging

from controllers.routes import handler_404, static_file
from urls import url_routes

logger = logging.getLogger(__name__)


def application(environ, start_response):
    url = environ.get('PATH_INFO')
    default_route = handler_404
    if url.startswith('/static/'):
        default_route = static_file
    url_route = url_routes.get(url, default_route)
    return url_route(environ, start_response)
