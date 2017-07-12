import json
import logging
import mimetypes
import os
import urllib.parse

import settings
import codecs

from controllers.template_render import Template

logger = logging.getLogger(__name__)


def handler_404(environ, start_response):
    start_response("404 Not Found", [("Content-type", "text/plain")])
    return ["404".encode("utf-8")]


def static_file(environ, start_response):
    full_path = os.path.normpath(os.path.abspath(os.path.join(settings.PROJECT_ROOT, environ.get('PATH_INFO')[1:])))
    if os.path.exists(full_path) and not os.path.isdir(full_path):
        content_type = mimetypes.guess_type(full_path)[0] or 'text/plain'
        with codecs.open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        start_response("200 OK", [("Content-type", content_type)])
        return [content.encode("utf-8")]
    return handler_404(environ, start_response)


def template_render_route(environ, start_response, path_to_template, **context):
    path_to_template = os.path.normpath(os.path.abspath(os.path.join(settings.PROJECT_ROOT, path_to_template)))
    if os.path.exists(path_to_template):
        with codecs.open(path_to_template, 'r', encoding='utf-8') as template_file:
            template = Template(template_file.read()).render(**context)
        start_response("200 OK", [("Content-type", "text/html; charset=UTF-8")])
        return [template.encode("utf-8")]
    return handler_404(environ, start_response)


def add_comment(environ, start_response):
    context = {
        "comment_sent": False
    }
    if environ.get('REQUEST_METHOD').upper() == 'GET':
        return template_render_route(environ, start_response, 'views/add_comment.html', **context)
    elif environ.get('REQUEST_METHOD').upper() == 'POST':
        content_len = int(environ['CONTENT_LENGTH']) if environ.get('CONTENT_LENGTH') else 0
        body = urllib.parse.parse_qs(environ['wsgi.input'].read(content_len).decode(), True) if content_len > 0 else {}
        print(body)
        context["comment_sent"] = True
        return template_render_route(environ, start_response, 'views/add_comment.html', **context)


def list_comments(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])
    return ["List comment!".encode("utf-8")]


def stat_comments(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])
    return ["Stat comment!".encode("utf-8")]


def index(environ, start_response):
    return template_render_route(environ, start_response, 'views/index.html')


def get_cities_json(environ, start_response):
    start_response("200 OK", [("Content-type", "application/json")])
    response = {
        "cities": [1, 2, 3]
    }
    return [json.dumps(response).encode("utf-8")]
