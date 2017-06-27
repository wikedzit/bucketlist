import json
from flask_testing import TestCase
from ...imports import app,api,ns,jwt, envi, databases
from ...v1.models import User

class TestAuthentication(TestCase):

    def create_app(self):
        envi("Testing")
        return app

    def setUp(self):
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_inputs_required_for_registration(self):
        payload = {'username': "twikedzi@gmail.com"}
        response = self.client.post("/auth/register", data=payload)
        res_message = response.data.decode('Utf-8')
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_validates_user_inputs_for_registration(self):
        payload = {'username': "twikedzi", "password":"admin"}
        response = self.client.post("/auth/register", data=payload)
        res_message = response.data.decode('Utf-8')
        message = res_message['message']
        self.assertEqual(message, "Username must be a valid email address")

    def test_user_can_register(self):
        payload = {'username': "jchambile@gmail.com", "password":"user"}
        response = self.client.post("/auth/register", data=payload)
        res_message = response.data.decode('Utf-8')
        message = res_message['message']
        self.assertEqual(response.status_code, 204)
        self.assertEqual(message, "User created")

    def test_no_ducplicated_usernames(self):
        payload = {'username':"swikedzi@gmail.com", "password" :"a133"}
        User(payload).store()
        response = self.client.post("/auth/register", data=payload)
        res_message = response.data.decode('Utf-8')
        message = res_message['message']
        self.assertEqual(message, "Username not available")

    def test_requires_username_and_password_to_login(self):
        payload = {'username': "twikedzi@gmail.com"}
        response = self.client.post("/auth/login", data=payload)
        res_message = response.data.decode('Utf-8')
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_user_can_login(self):
        response = self.client.get("/bucketlists/")
        payload = {'username': 'twikedzi@gmail.com', 'password': 'admin'}
        #response = self.app.post('auth/login')
        #assert_in("BucketList", response.data.decode('Utf-8'))
        self.assertEqual(200, response.status_code)
        #datadict = json.loads(credentials.data)
        #token = datadict['Token']
        #print(token)
        #self.assertEqual(response.data, True)
