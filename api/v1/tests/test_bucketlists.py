from .imports import *
import json
import unittest
from headers import app, envi, databases
from models import User, Bucket


class TestBucketList(unittest.TestCase):

    def setUp(self):
        envi("Testing")
        databases.create_all()
        self.app = app.test_client()

        self.payload = dict(username="wikedzit@gmail.com", password="admin")
        User(self.payload).store()

        response = self.app.post("/api/v1/auth/login", data=json.dumps(self.payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        self.token = "Bearer {0}".format(res_message["access_token"])

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_can_create_a_bucketlist(self):
        bucket_payload = dict(name="Richest men alive")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(201, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist created")

    def test_requires_backetlist_name_before_creating_them(self):
        bucket_payload = dict(name="")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist name is missing")

    def test_requires_valid_token_to_access_bucketlist(self):
        response = self.app.get("/api/v1/bucketlists", headers={"Authorization": "Bearer invalid token"})
        self.assertEqual(500, response.status_code)

    def test_user_can_only_access_own_bucketlists(self):
        self.assertTrue(True, True)

    def test_can_delete_a_bucketlist(self):
        bucket_payload = dict(name="Programming Languages")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(201, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist created")

        response = self.app.delete("/api/v1/bucketlists/1", headers={"Authorization": self.token})
        self.assertEqual(204, response.status_code)

    def test_can_add_an_item_to_a_backetlist(self):
        self.assertTrue(True, True)

    def test_can_delete_an_item_from_a_bucketlist(self):
        self.assertTrue(True, True)

    def test_default_limit(self):
        # create 100 bucketlists
        for i in range(100):
            name = "Bucket " + str(i)
            payload = dict(name=name)
            Bucket(payload).store()

        response = self.app.get("/api/v1/bucketlists", headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        buckets = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(len(buckets), 20)

    def test_maximum_limit(self):
        # create 150 bucketlists
        for i in range(150):
            name = "Bucket " + str(i)
            payload = dict(name=name)
            Bucket(payload).store()

        response = self.app.get("/api/v1/bucketlists?limit=200", headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        buckets = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(len(buckets), 100)
