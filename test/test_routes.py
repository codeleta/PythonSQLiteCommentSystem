import json
import unittest
import urllib.error
from urllib.request import urlopen
from threading import Thread

import settings
from server import run_handle_request


class TestViews(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://{}:{}'.format(settings.HOST, settings.PORT)
        self.server = Thread(target=run_handle_request)
        self.server.daemon = True
        self.server.start()

    def test_add_comment_route(self):
        response = urlopen('{}/comment/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)
        response.close()

    def test_list_comments_route(self):
        response = urlopen('{}/view/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)
        response.close()

    def test_stat_comments_route(self):
        response = urlopen('{}/stat/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)
        response.close()

    def test_404_route(self):
        with self.assertRaises(urllib.error.HTTPError):
            urlopen('{}/not_exists_url/'.format(self.base_url))

    def test_cities_json_route(self):
        with self.assertRaises(urllib.error.HTTPError):
            urlopen('{}/get_cities/'.format(self.base_url))
        response = urlopen('{}/get_cities/?region=1'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)
        json_response = json.loads(response.read())
        self.assertIsInstance(json_response, list)
        response.close()

    def test_static_file_route(self):
        response = urlopen('{}/static/css/style.css'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)
        response.close()

    def test_404_static_file_route(self):
        with self.assertRaises(urllib.error.HTTPError):
            urlopen('{}/static/css/no_exist_file.css'.format(self.base_url))
