from .imports import *
import json
import unittest
from headers import envi, databases
from app import app, User


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        envi("Testing")
        databases.create_all()
        self.app = app.test_client()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_inputs_required_for_registration(self):
        payload = dict(username="twikedzi@gmail.com")
        response = self.app.post("/api/v1/auth/register", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_validates_user_inputs_for_registration(self):
        payload = dict(username="twikedzi", password="admin")
        response = self.app.post("/api/v1/auth/register", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Username must be a valid email address")

    def test_checks_for_empty_username_during_registration(self):
        payload = dict(username="", password="admin")
        response = self.app.post("/api/v1/auth/register", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        self.assertEqual(400, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_checks_for_empty_password_during_registration(self):
        payload = dict(username="tbangu@gmail.com", password="")
        response = self.app.post("/api/v1/auth/register", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        self.assertEqual(400, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")


    def test_user_can_register(self):
        payload = dict(username="jchambile@gmail.com", password="user")
        response = self.app.post("/api/v1/auth/register", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(response.status_code, 201)
        self.assertEqual(message, "User created")

    def test_no_ducplicated_usernames(self):
        payload = dict(username="swikedzi@gmail.com", password="a133")
        User(payload).store()
        response = self.app.post("/api/v1/auth/register", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Username already used. Use a different name to register")

    def test_requires_username_and_password_to_login(self):
        payload = dict(username="twikedzi@gmail.com")
        response = self.app.post("/api/v1/auth/login", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Both username and password are required")

    def test_user_can_login(self):
        payload = dict(username='admin@gmail.com', password='admin')
        User(payload).store()
        response = self.app.post('api/v1/auth/login', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.assertIn('access_token', res_message.keys())
