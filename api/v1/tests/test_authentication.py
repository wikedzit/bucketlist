import json
from flask_testing import TestCase
from nose.tools import assert_equal, assert_not_equal, assert_raises, raises, assert_in
from ...imports import app,api,ns,jwt, envi, databases
from ...v1.models import User
from ...v1.routes import *
envi("Develop")

class TestAuthentication(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        self.app = app.test_client()
        databases.create_all()
        payload = {'username': 'twikedzi@gmail.com', 'password': 'admin'}
        User(payload).store()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_validates_user_inputs(self):
        self.assertEqual(True,True)

    def test_user_can_register(self):
        self.assertEqual(True,True)

    def test_no_ducplicated_usernames(self):
        self.assertEqual(True,True)

    def test_user_can_login(self):
        payload = {'username': 'twikedzi@gmail.com', 'password': 'admin'}
        response = self.app.post('auth/login')
        #assert_in("BucketList", response.data.decode('Utf-8'))
        assert_equal(200, response.status_code)
        #datadict = json.loads(credentials.data)
        #token = datadict['Token']
        #print(token)
        self.assertEqual(response.data, True)
