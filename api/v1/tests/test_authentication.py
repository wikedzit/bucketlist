import imports
import json
import unittest

from api import app
from headers import envi

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        envi("Testing")
        databases.create_all()
        self.app = app.test_client()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_inputs_required_for_registration(self):
        payload = {'username': "twikedzi@gmail.com"}
        response = self.app.post("/api/v1/auth/register", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_validates_user_inputs_for_registration(self):
        payload = {'username': "twikedzi", "password":"admin"}
        response = self.app.post("/api/v1/auth/register", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Username must be a valid email address")

    def test_user_can_register(self):
        payload = {'username': "jchambile@gmail.com", "password":"user"}
        response = self.app.post("/api/v1/auth/register", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(response.status_code, 204)
        self.assertEqual(message, "User created")

    def test_no_ducplicated_usernames(self):
        payload = {'username':"swikedzi@gmail.com", "password" :"a133"}
        User(payload).store()
        response = self.app.post("/api/v1/auth/register", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Username not available") #Username is already used .......

    def test_requires_username_and_password_to_login(self):
        payload = {'username': "twikedzi@gmail.com"}
        response = self.app.post("/api/v1/auth/login", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_user_can_login(self):
        payload = {'username': 'admin@gmail.com', 'password': 'admin'}
        payload = dict(username='admin@gmail.com', password='admin')
        User(payload).store()
        response = self.app.post('api/v1/auth/login', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.assertIn('access_token', res_message.keys())

        #assert_in("BucketList", response.data.decode('Utf-8'))
        #self.assertEqual(200, response.status_code)
        #datadict = json.loads(credentials.data)
        #token = datadict['Token']
        #print(token)
        #self.assertEqual(response.data, True)
