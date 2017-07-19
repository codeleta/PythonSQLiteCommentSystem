import json
import logging
import mimetypes
import os
import urllib.parse

import settings
import codecs

from controllers.template_render import Template
from db.models import Region, City
from db.models.comment import Comment
from db.sql import SqlQuery

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
        "regions": SqlQuery(Region).select("*").fetchall(),
        "region_id": 0
    }
    if environ.get('REQUEST_METHOD').upper() == 'GET':
        return template_render_route(environ, start_response, 'views/add_comment.html', **context)
    elif environ.get('REQUEST_METHOD').upper() == 'POST':
        content_len = int(environ['CONTENT_LENGTH']) if environ.get('CONTENT_LENGTH') else 0
        body = urllib.parse.parse_qs(environ['wsgi.input'].read(content_len).decode(), True) if content_len > 0 else {}
        comment = Comment(body)
        saved = comment.save()
        context.update({
            "comment_sent": saved,
            "comment": comment if not saved else {},
            "errors": comment.errors
        })
        if comment["region_id"] and not saved:
            region_id = int(comment["region_id"])
            context.update({
                "cities": SqlQuery(City).select("*").where(**{"cities.region_id": region_id}).fetchall(),
                "region_id": region_id,
                "city_id": comment["city_id"]
            })
        return template_render_route(environ, start_response, 'views/add_comment.html', **context)


def list_comments(environ, start_response):
    if environ.get('REQUEST_METHOD').upper() == 'GET':
        fields = [
            'comments.id', 'comments.first_name', 'comments.last_name', 'comments.text',
            'comments.middle_name', 'comments.phone', 'comments.email',
            'comments.city_id', 'cities.title AS city_title'
        ]
        qs = SqlQuery(Comment).select(fields).left_join("city_id").fetchall()
        context = {'comments': qs}
        return template_render_route(environ, start_response, 'views/list_comments.html', **context)
    elif environ.get('REQUEST_METHOD').upper() == 'DELETE':
        start_response("200 OK", [("Content-type", "application/json")])
        content_len = int(environ['CONTENT_LENGTH']) if environ.get('CONTENT_LENGTH') else 0
        body = urllib.parse.parse_qs(environ['wsgi.input'].read(content_len).decode(), True) if content_len > 0 else {}
        deleted = Comment(body).delete()
        return [json.dumps({"success": deleted}).encode("utf-8")]


def stat_comments(environ, start_response):
    GET_params = urllib.parse.parse_qs(environ["QUERY_STRING"], True)
    if GET_params.get('region'):
        fields = [
            'cities.id', 'cities.title', 'COUNT(comments.id) AS comments_count'
        ]
        query = SqlQuery(City).select(fields).left_join("city_id", Comment)
        query = query.where(**{"cities.region_id__in": GET_params["region"]}).group_by("cities.id")
        qs = query.fetchall()
        context = {'cities': qs}
    else:
        fields = [
            'regions.id', 'regions.title', 'COUNT(comments.id) AS comments_count'
        ]
        query = SqlQuery(Region).select(fields).left_join("region_id", City).left_join("city_id", Comment)
        query = query.group_by("regions.id").where(True, **{"comments_count__gt": 5})
        qs = query.fetchall()
        context = {'regions': qs}
    return template_render_route(environ, start_response, 'views/stat_regions.html', **context)


def index(environ, start_response):
    return template_render_route(environ, start_response, 'views/index.html')


def get_cities_json(environ, start_response):
    GET_params = urllib.parse.parse_qs(environ["QUERY_STRING"], True)
    if GET_params.get('region'):
        start_response("200 OK", [("Content-type", "application/json")])
        query = SqlQuery(City).select("*").where(**{"cities.region_id__in": GET_params["region"]})
        qs = query.fetchall()
        json_qs = json.dumps(qs, default=lambda x: x.values)
        return [json_qs.encode("utf-8")]
    return handler_404(environ, start_response)
