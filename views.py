import json
import logging


logger = logging.getLogger(__name__)


def handler_404(environ, start_response):
    start_response("404 Not Found", [("Content-type", "text/plain")])
    return ["404".encode("utf-8")]


def add_comment(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])
    return ["Add comment!".encode("utf-8")]


def list_comments(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])
    return ["List comment!".encode("utf-8")]


def stat_comments(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])
    return ["Stat comment!".encode("utf-8")]


def get_cities_json(environ, start_response):
    start_response("200 OK", [("Content-type", "application/json")])
    response = {
        "cities": [1, 2, 3]
    }
    return [json.dumps(response).encode("utf-8")]