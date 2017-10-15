import json
import unittest
from datetime import timedelta
import time
from ..headers import envi, databases
from ..endpoints import app, User, Bucket


class TestToken(unittest.TestCase):
    def setUp(self):
        envi("Testing")
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=5)
        databases.create_all()
        self.app = app.test_client()

        self.payload = dict(username="wikedzit@gmail.com", password="admin")
        User(self.payload).store()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_token_expires(self):
        response = self.app.post("/api/v1/auth/login", data=json.dumps(self.payload), headers={'Content-Type': 'application/json'})
        res_message = json.loads(response.data.decode('Utf-8'))
        token = "Bearer {0}".format(res_message["access_token"])

        response = self.app.get("/api/v1/bucketlists", headers={"Authorization": token})
        self.assertEqual(200, response.status_code)

        time.sleep(6)

        response = self.app.get("/api/v1/bucketlists", headers={"Authorization": token})
        self.assertEqual(500, response.status_code)


if __name__ == '__main__':
    unittest.main()
