import json
from flask_testing import TestCase
from ...imports import app,jwt, envi, databases
from ...v1.models import User

class TestBucketList(TestCase):
    def create_app(self):
        envi("Testing")
        return app

    def setUp(self):
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_requires_backetlist_name_before_creating_them(self):
        payload = {"name":""}
        response = self.client.post("/bucketlists", data=payload)
        res_message = response.data.decode('Utf-8')
        message = res_message['message']
        self.assertEqual(message, "Bucketlist name is missing")

    def test_validates_token(self):
        assert_equal(True, True)

    def test_requires_token_to_access_bucketlists(self):
        assert_equal(True,True)

    def test_requires_active_user_to_add_bucketlists(self):
        assert_equal(True,True)

    def test_user_can_only_access_own_bucketlists(self):
        assert_equal(True,True)

    def test_can_add_bucketlist(self):
        assert_equal(True,True)

    def test_can_delete_a_bucketlist(self):
        assert_equal(True, True)

    def test_can_add_an_item_to_a_backetlist(self):
        assert_equal(True,True)

    def test_can_add_an_item_to_a_backetlist(self):
        assert_equal(True,True)

    def test_can_delete_an_item_from_a_bucketlist(self):
        assert_equal(True,True)

    def test_pagination_limit_is_validated_to_number(self):
        assert_equal(True,True)

    def test_default_limit(self):
        assert_equal(True,True)

    def test_maximum_limit(self):
        assert_equal(True,True)

    def test_search_string_is_a_clean_string(self):
        assert_equal(True,True)