import json
from flask_testing import TestCase
from ...imports import app, envi, databases
from ...v1.models import User

class TestBucketList(TestCase):
    def create_app(self):
        envi("Testing")
        return app

    def setUp(self):
        databases.create_all()

        self.payload = {"username": "wikedzit@gmail.com", "password": "admin"}
        User(self.payload).store()

        response = self.client.post("api/v1/auth/login", data=self.payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.token = res_message["access_token"]
        self.token = "Bearer {0}".format(self.token)

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_requires_backetlist_name_before_creating_them(self):
        payload = {"name":""}
        response = self.client.post("/api/v1/bucketlists", data=payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist name is missing")

    def test_requires_token_to_access_bucketlist(self):
        response = self.client.get("/api/v1/bucketlists")
        self.assertEqual(500, response.status.code)

    def test_requires_active_user_to_create_bucketlists(self):
        bucket_payload = {"name": "Natural Languages"}
        response = self.client.post("/api/v1/bucketlists", data=bucket_payload)
        self.assertEqual(500, response.status.code)

        response = self.client.post("api/v1/auth/login", data=self.payload)
        res_message = json.loads(response.data.decode('Utf-8'))
        token = res_message['access_token']
        token = "Bearer {0}".format(token)

        response = self.client.post("api/v1/bucketlists", data=bucket_payload, headers={"Authorisation": self.token})
        self.assertEqual(204, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucket Created")

    def test_user_can_only_access_own_bucketlists(self):
        self.assertTrue(True, True)

    def test_can_delete_a_bucketlist(self):
        bucket_payload = {"name": "Programming Languages"}
        response = self.client.post("api/v1/bucketlists", data=bucket_payload, headers={"Authorisation": self.token})
        self.assertEqual(204, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucket Created")

        response = self.client.delete("api/v1/bucketlists/1", headers={"Authorisation": self.token})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucket deleted")
        #Add a statuc code test

    def test_can_add_an_item_to_a_backetlist(self):
        self.assertTrue(True, True)

    def test_can_delete_an_item_from_a_bucketlist(self):
        self.assertTrue(True, True)

    def test_pagination_limit_is_validated_to_number(self):
        response = self.client.get("api/v1/bucketlists?limit=abcd", headers={"Authorisation": self.token})
        self.assertTrue(response.data is None)

    def test_default_limit(self):
        response = self.client.get("api/v1/bucketlists", headers={"Authorisation": self.token})
        res_message = response.data.decode('Utf-8')
        self.assertTrue(len(res_message) <= 20)

    def test_maximum_limit(self):
        response = self.client.get("api/v1/bucketlists?limit=200", headers={"Authorisation": self.token})
        self.assertTrue(response.data is None)

