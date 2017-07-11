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

    def test_add_comment_view(self):
        response = urlopen('{}/comment/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)

    def test_list_comments_view(self):
        response = urlopen('{}/view/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)

    def test_stat_comments_view(self):
        response = urlopen('{}/stat/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)

    def test_404_view(self):
        with self.assertRaises(urllib.error.HTTPError):
            urlopen('{}/'.format(self.base_url))

    def test_cities_json(self):
        response = urlopen('{}/get_cities/'.format(self.base_url))
        self.assertEqual(response.getcode(), 200)
        json_response = json.loads(response.read())
        self.assertIsInstance(json_response, dict)
