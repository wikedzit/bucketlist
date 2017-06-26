from flask import jsonify, request, abort
from api.imports import app, api, ns, databases,jwt
from api.v1.models import User, Bucket, Item
from flask_restplus import Resource, fields, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

databases.create_all()

parser = reqparse.RequestParser()
parser.add_argument('q', type=str, help='Search word is a string')
parser.add_argument('limit', type=int, help='Limit can only be a number')
parser.add_argument('username')
parser.add_argument('password')

item = api.model('Item', {
    'id': fields.Integer(readOnly=True, description='The Item unique identifier'),
    'name': fields.String(required=True, description='The Item name'),
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822'),
    'done': fields.Boolean
})

bucket = api.model('Bucket', {
    'id': fields.Integer(readOnly=True, description='The bucket unique identifier'),
    'name': fields.String(required=True, description='The bucket name'),
    'items': fields.List(fields.Nested(item)),
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822'),
})


user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The username'),
    'buckets': fields.List(fields.Nested(bucket)),
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822'),
})

auth = api.model('User', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The Password')
})


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 101,
        'msg': 'The token has expired'
    }), 200


@ns.route('/auth/login')
class Auth(Resource):
    """Shows a list of users for the authenticated user, and lets you POST to add new users"""
    @ns.doc('login_user')
    @ns.response(200, 'User Logged in')
    @ns.expect(auth)
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if username and password:
            usr = User.login(username, password)
            if usr:
                return {'access_token': create_access_token(identity=usr.id)}, 200
            return {"message": "Incorrect username or password"}, 404
        else:
            return {"message": "Both username and password are required"}, 404


@ns.route('/auth/register')
class Users(Resource):
    """Shows a list of users for the authenticated user, and lets you POST to add new users"""
    @ns.doc('register_user')
    @ns.expect(user)
    @ns.marshal_with(user, code=201)
    def post(self):
        """Register a new user"""
        usr = User(api.payload)
        usr.store()
        return usr


@ns.route('/bucketlists')
class BucketList(Resource):
    """Shows a list of buckets for the authenticated user, and lets you POST to add new buckets"""
    @ns.doc('list_buckets')
    @ns.marshal_list_with(bucket)
    @jwt_required
    def get(self):
        """List all buckets"""
        args = parser.parse_args()
        lmt = 0
        qword = None
        if args['limit']:
            lmt = int(args['limit'])

        if args['q']:
            qword = args['q']
        # user = User.first()
        buckets = Bucket.all(lmt=lmt, q=qword)
        return buckets

    @ns.doc('create_bucket')
    @ns.expect(bucket)
    @ns.marshal_with(bucket, code=201)
    def post(self):
        """Create a new bucket"""
        buck = Bucket(api.payload)
        if buck.store():
            return buck, 201
        return {'message': 'Bucket could not be created'}, 417


@ns.route('/bucketlists/<int:id>')
@ns.response(404, 'Backet not found')
@ns.param('id', 'The bucket identifier')
class Buckets(Resource):
    """Show a single bucket and lets you update or delete them"""
    @ns.doc('get_bucket')
    @ns.marshal_with(bucket)
    def get(self, id):
        """Fetch a given bucket"""
        buck = Bucket.find(id)
        if buck:
            return buck, 200
        else:
            return {'message': 'Bucket not found'}, 404

    @ns.doc('delete_backet')
    @ns.response(204, 'Bucket deleted')
    def delete(self, id):
        """Delete a bucket given its identifier"""
        buck = Bucket.find(id)
        if buck:
            buck.delete()
            return {'message': 'Bucket deleted'}, 204
        else:
            return {'message': 'Bucket not found'}, 404

    @ns.expect(bucket)
    @ns.marshal_with(bucket)
    def put(self, id):
        """Update a bucket given its identifier"""
        buck = Bucket.find(id)
        if buck.put(api.payload):
            return buck, 200
        else:
            return {'message': 'Bucket could not be updated'}, 417


@ns.route('/bucketlists/<int:id>/items')
@ns.param('id', 'The bucket identifier')
class ItemsList(Resource):
    """Shows a list of items in a given bucket, and lets you POST to add new items"""
    @ns.doc('list_items')
    @ns.marshal_list_with(item)
    def get(self, id):
        """List all items"""
        items = Bucket.find(id).items
        return items

    @ns.doc('create_items')
    @ns.expect(item)
    @ns.marshal_with(item, code=201)
    def post(self, id):
        """Create a new item"""
        api.payload.update({'bucket_id': id})
        itm = Item(api.payload)
        itm.store()
        return itm, 201


@ns.route('/bucketlists/<int:id>/items/<int:item_id>')
@ns.response(404, 'Bucket Item not found')
@ns.param('id', 'The Bucket identifier')
@ns.param('item_id', 'The Item identifier')
class Items(Resource):
    """Show a single bucket item and lets you update or delete them"""
    @ns.doc('get_bucket_item')
    @ns.marshal_with(item)
    def get(self, id, item_id):
        """Fetch a given bucket"""
        itm = Item.where(id=item_id, bucket_id=id).first()
        return itm

    @ns.doc('delete_backet_item')
    @ns.response(204, 'Item deleted')
    def delete(self, id, item_id):
        """Delete a bucket given its identifier"""
        itm = Item.where(id=item_id, bucket_id=id).first()
        if itm:
            itm.delete()
            return {'message': 'Item deleted'}, 204
        else:
            return {'message': 'Item not found'}, 404

    @ns.expect(bucket)
    @ns.marshal_with(bucket)
    def put(self, id, item_id):
        """Update an Item given a bucket identifier and Item identifier"""
        itm = Item.where(id=item_id, bucket_id=id).first()
        if itm.put(api.payload):
            return itm, 200
        else:
            return {'message': 'Item could not be updated'}, 404