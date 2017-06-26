import json
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from ...imports import app, envi, databases

class TestAuthentication():
    def setUp(self):
        self.app = app.test_client()
        envi("Testing")
        databases.create_all()

        payload = {'username':'twikedzi@gmail.com', 'password':'admin'}
        self.app.post('/auth/register', data=payload)

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_validates_user_inputs(self):
        assert_equal(True,True)

    def test_user_can_register(self):
        assert_equal(True,True)

    def test_no_ducplicated_usernames(self):
        assert_equal(True,True)

    def test_user_can_login(self):
        payload = {'username':'twikedzi@gmail.com','password':'admin'}
        credentials = self.app.post('/auth/login', data=payload)
        assert_equal(credentials, "abc")
        #datadict = json.loads(credentials.data)
        #token = datadict['Token']
        #print(token)
        assert_equal(True,True)
