from .imports import *
import json
import unittest
from headers import envi, databases
from endpoints import app, User, Bucket


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
        self.postheader = {'Content-Type':'', 'Authorization':self.token}

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_payload_required_for_posting(self):
        response = self.app.post("/api/v1/bucketlists", data=json.dumps({}), headers=self.postheader)
        self.assertEqual(400, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Payload missing")

    def test_can_create_a_bucketlist(self):
        bucket_payload = dict(name="Richest men alive")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(201, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist created")

    def test_can_edit_a_bucketlist(self):
        bucket_payload = dict(name="Cohort 17")
        self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        r = self.app.get("/api/v1/bucketlists/1", headers={"Authorization": self.token})
        res_message = json.loads(r.data.decode('Utf-8'))
        self.assertEqual(res_message['name'], "Cohort 17")

        update_payload = dict(name="Cohort Seventeen")
        response = self.app.put("/api/v1/bucketlists/1", data=json.dumps(update_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(res_message['message'], "Bucketlist updated")

        r = self.app.get("/api/v1/bucketlists/1", headers={"Authorization": self.token})
        res_message = json.loads(r.data.decode('Utf-8'))
        self.assertEqual(res_message['name'], "Cohort Seventeen")


    def test_cant_edit_a_bucketlist_with_the_same_name(self):
        bucket_payload = dict(name="Computer Science")
        self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})

        update_payload = dict(name="Computer Science")
        response = self.app.put("/api/v1/bucketlists/1", data=json.dumps(update_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(response.status_code, 406)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(res_message['message'], "Bucketlist name has not changed, update not allowed")

    def test_requires_backetlist_name_before_creating_them(self):
        bucket_payload = dict(name="")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist name is missing")

    def test_requires_valid_token_to_access_bucketlist(self):
        response = self.app.get("/api/v1/bucketlists", headers={"Authorization": "invalid token"})
        self.assertEqual(500, response.status_code)


    def test_user_can_only_access_own_bucketlists(self):
        bucket_payload = dict(name="Richest men alive")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(201, response.status_code)

        alien_payload = dict(username="taracha@gmail.com", password="super")
        User(alien_payload).store()

        response = self.app.post("/api/v1/auth/login", data=json.dumps(alien_payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        alien_token = "Bearer {0}".format(res_message["access_token"])

        response = self.app.get("/api/v1/bucketlists/1", headers={"Authorization": alien_token})
        self.assertEqual(404, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.assertTrue(res_message['name'] is None)

    def test_can_delete_a_bucketlist(self):
        bucket_payload = dict(name="Programming Languages")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(201, response.status_code)
        res_message = json.loads(response.data.decode('Utf-8'))
        message = res_message['message']
        self.assertEqual(message, "Bucketlist created")

        response = self.app.delete("/api/v1/bucketlists/1", headers={"Authorization": self.token})
        self.assertEqual(200, response.status_code)

    def test_can_add_an_item_to_a_backetlist(self):
        bucket_payload = dict(name="New Testament")
        self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})

        item_payload = dict(name="Mathew")
        response = self.app.post("/api/v1/bucketlists/1/items", data=json.dumps(item_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        res_message = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(res_message['message'], "Added item to bucket 1")

    def test_can_delete_an_item_from_a_bucketlist(self):
        bucket_payload = dict(name="Old Testament")
        self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})

        item_payload = dict(name="Genesis")
        self.app.post("/api/v1/bucketlists/1/items", data=json.dumps(item_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})

        response = self.app.get("/api/v1/bucketlists/1/items/1",  headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        string_res_message = response.data.decode('Utf-8')
        self.assertIn("Genesis", string_res_message)

        response = self.app.delete("/api/v1/bucketlists/1/items/1",  headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        string_res_message = json.loads(response.data.decode('Utf-8'))
        self.assertEquals("Item deleted", string_res_message['message'])


    def test_default_limit(self):
        # create 100 bucketlists
        for i in range(100):
            name = "Bucket " + str(i)
            payload = dict(name=name)
            Bucket(payload, uid=1).store()

        response = self.app.get("/api/v1/bucketlists", headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        buckets = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(len(buckets), 20)

    def test_maximum_limit(self):
        # create 150 bucketlists
        for i in range(150):
            name = "Bucket " + str(i)
            payload = dict(name=name)
            Bucket(payload, uid=1).store()

        response = self.app.get("/api/v1/bucketlists?limit=200", headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        buckets = json.loads(response.data.decode('Utf-8'))
        self.assertEqual(len(buckets), 100)

    def test_can_search_a_bucketlist_by_name_key(self):
        bucket_payload = dict(name="Laravel Framework")
        response = self.app.post("/api/v1/bucketlists", data=json.dumps(bucket_payload), headers={'Content-Type': 'application/json', "Authorization": self.token})

        response = self.app.get("/api/v1/bucketlists?q=work", headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        buckets = json.loads(response.data.decode('Utf-8'))

        self.assertEqual(buckets[0]['name'], "Laravel Framework")


if __name__ == '__main__':
    unittest.main()