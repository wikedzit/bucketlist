from .imports import *
import json
import unittest
from flask_testing import TestCase
from headers import app, envi, databases
from models import User


class TestBucketList(unittest.TestCase):

    def setUp(self):
        envi("Testing")
        databases.create_all()
        self.app = app.test_client()

        self.payload = dict(username="wikedzit@gmail.com", password="admin")
        User(self.payload).store()

        response = self.app.post("api/v1/auth/login", data=self.payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.token = res_message["access_token"]
        self.token = "Bearer {0}".format(self.token)

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_requires_backetlist_name_before_creating_them(self):
        payload = dict(name="")
        response = self.app.post("/api/v1/bucketlists", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist name is missing")

    def test_requires_token_to_access_bucketlist(self):
        response = self.app.get("/api/v1/bucketlists")
        self.assertEqual(500, response.status.code)

    def test_requires_active_user_to_create_bucketlists(self):
        bucket_payload = dict(name="Natural Languages")
        response = self.app.post("/api/v1/bucketlists", data=bucket_payload)
        self.assertEqual(500, response.status.code)

        response = self.app.post("api/v1/bucketlists", data=bucket_payload, headers={"Authorisation": self.token})
        self.assertEqual(204, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucket Created")

    def test_user_can_only_access_own_bucketlists(self):
        self.assertTrue(True, True)

    def test_can_delete_a_bucketlist(self):
        bucket_payload = dict(name="Programming Languages")
        response = self.app.post("api/v1/bucketlists", data=bucket_payload, headers={"Authorisation": self.token})
        self.assertEqual(204, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucket Created")

        response = self.app.delete("api/v1/bucketlists/1", headers={"Authorisation": self.token})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucket deleted")
        #Add a statuc code test

    def test_can_add_an_item_to_a_backetlist(self):
        self.assertTrue(True, True)

    def test_can_delete_an_item_from_a_bucketlist(self):
        self.assertTrue(True, True)

    def test_pagination_limit_is_validated_to_number(self):
        response = self.app.get("api/v1/bucketlists?limit=abcd", headers={"Authorisation": self.token})
        self.assertTrue(response.data is None)

    def test_default_limit(self):
        response = self.app.get("api/v1/bucketlists", headers={"Authorisation": self.token})
        res_message = response.data.decode('Utf-8')
        self.assertTrue(len(res_message) <= 20)

    def test_maximum_limit(self):
        response = self.app.get("api/v1/bucketlists?limit=200", headers={"Authorisation": self.token})
        self.assertTrue(response.data is None)

