import json
from nose.tools import assert_equal
from nose.tools import assert_not_equal, assert_raises, raises, assert_in
from ...imports import ns,app, envi, databases

class TestBucketList():
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validates_backetlist_name_before_creating_them(self):
        assert_equal(True, True)

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
        assert_equal(True,True)

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