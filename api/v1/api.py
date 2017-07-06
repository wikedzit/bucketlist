import re
from flask import jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, get_jwt_identity
from flask_restplus import Resource, fields, reqparse

from headers import app, api, ns, databases
from models import User, Bucket, Item

jwt = JWTManager(app)
databases.create_all()

parser = reqparse.RequestParser()
parser.add_argument('q', type=str, help='Search word is a string')
parser.add_argument('limit', type=int, help='Limit can only be a number')
parser.add_argument('page', type=int, help='page can only be a number')
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
    'created_by': fields.Integer(readOnly=True, description='The bucket owner', attribute='user_id'),
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

@jwt.invalid_token_loader
def invalid_token_loader():
    return jsonify({
        'status': 406,
        'sub_status': 101,
        'msg': 'The token is invalid'
    }), 200


@ns.route('/auth/register')
class Users(Resource):
    """Shows a list of users for the authenticated user, and lets you POST to add new users"""
    @ns.doc('register_user')
    @ns.expect(user)
    def post(self):
        """Register a new user"""
        if not api.payload:
            return {"message": "Payload missing"}, 400 #this is a bad request

        data = api.payload.keys()
        if ('username' in data) and ('password' in data):
            email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.match(email, api.payload['username']):
                user_exists = User.where(username=api.payload['username']).first()

                if user_exists:
                    return {"message": "Username already used. Use a different name to register"}, 406  # This is not acceptable
                else:
                    usr = User(api.payload)
                    usr.store()
                    return {"message": "User created"}, 201  # Resource is created and saved
            else:
                return {"message": "Username must be a valid email address"}, 400  # Bad request
        else:
            return {"message": "Both username and password are required"}, 400  # Bad request


@ns.route('/auth/login')
class Auth(Resource):
    """Shows a list of users for the authenticated user, and lets you POST to add new users"""
    @ns.doc('login_user')
    @ns.response(200, 'User Logged in')
    @ns.expect(auth)
    def post(self):
        if not api.payload:
            return {"message": "Payload missing"}, 400  # Bad request
        data = api.payload.keys()
        if ('username' in data) and ('password' in data):
            email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            username = api.payload['username']
            password = api.payload['password']

            if re.match(email, username):
                usr = User.login(username, password)
                if usr:
                    access_token = create_access_token(identity=usr.id)
                    resp = jsonify({'login': True})
                    #set_access_cookies(resp, access_token)
                    return {'access_token': access_token, 'login': True}, 200  # OK
                    #return {'login': True}, 200
                return {"message": "User not found"}, 404  #Reource not found
            else:
                return {"message": "Username must be a valid email address"}, 400  # Bad request
        else:
            return {"message": "Both username and password are required"}, 400  # Bad request

@ns.route('/bucketlists')
class BucketList(Resource):
    """Shows a list of buckets for the authenticated user, and lets you POST to add new buckets"""
    @ns.doc('list_buckets')
    @ns.marshal_list_with(bucket)
    @jwt_required
    def get(self):
        """List all buckets"""
        args = parser.parse_args()
        lmt = 20
        qword = None
        page=1
        if args['limit']:
            lmt = int(args['limit'])
            if lmt < 1:
                lmt = 20
            if lmt > 100:
                lmt = 100

        if args['q']:
            qword = args['q']
            if qword is None or qword == "":
                qword = None

        if args['page']:
            page = int(args['page'])
            if page < 1:
                page = 1

        user_id = get_jwt_identity()
        buckets = Bucket.all(lmt=lmt, page=page, q=qword, uid=user_id)
        return buckets, 200  # OK

    @ns.doc('create_bucket')
    @ns.expect(bucket)
    @jwt_required
    def post(self):
        """Create a new bucket"""
        try:
            if not api.payload:
                return {"message": "Payload missing"}, 400  # Bad request

            data = api.payload.keys()
            if ('name' in data) and (not api.payload["name"].strip() == ""):
                bucket_exists = Bucket.where(name=api.payload['name'].strip()).first()

                if bucket_exists:
                    return {'message': 'Bucket name already exists. Choose a different name to create a bucket'}, 406

                user_id = get_jwt_identity()
                buck = Bucket(api.payload, uid=user_id)
                if buck.store():
                    return {'message': 'Bucketlist created'}, 201
                else:
                    return {'message': 'Bucketlist could not be created'}, 500  # Error on server
            else:
                return {'message': 'Bucketlist name is missing'}, 400  # Bad request
        except:
            return {'message': 'An error has occured, could not create a bucketlist'}, 500  #Error on server


@ns.route('/bucketlists/<int:id>')
@ns.response(404, 'Backet not found')
@ns.param('id', 'The bucket identifier')
class Buckets(Resource):
    """Show a single bucket and lets you update or delete them"""
    @ns.doc('get_bucket')
    @ns.marshal_with(bucket)
    @jwt_required
    def get(self, id):
        """Fetch a given bucket"""
        user_id = get_jwt_identity()
        buck = Bucket.find(id, user_id)
        if buck:
            return buck, 200
        else:
            return None, 404

    @ns.doc('delete_backet')
    @ns.response(204, 'Bucket deleted')
    @jwt_required
    def delete(self, id):
        """Delete a bucket given its identifier"""
        buck = Bucket.find(id)
        if buck:
            buck.delete()
            return {'message': 'Bucketlist deleted'}, 204
        else:
            return {'message': 'Bucketlist not found'}, 404

    @ns.expect(bucket)
    @jwt_required
    def put(self, id):
        """Update a bucketlist given its identifier"""
        if not api.payload:
            return {"message": "Payload missing"}, 400  # Bad request

        user_id = get_jwt_identity()
        buck = Bucket.find(id, user_id)
        if buck:
            data = api.payload.keys()
            if 'name' in data:
                name = api.payload["name"].strip()
                # Check if there are changes
                if buck.name == name:
                    return {"message": "Bucketlist name has not changed, update not allowed"}, 406  # Not allowed
                if name != "":
                    if name != buck.name:
                        buck.put(api.payload)
                        return {"message": "Bucketlist updated"}, 200
            return {'message': 'Bucketlist name is required'}, 400  # Bad request
        else:
            return {'message': 'Bucketlist not found in your collection'}, 404

@ns.route('/bucketlists/<int:id>/items')
@ns.param('id', 'The bucket identifier')
class ItemsList(Resource):
    """Shows a list of items in a given bucket, and lets you POST to add new items"""
    @ns.doc('list_items')
    @ns.marshal_list_with(item)
    @jwt_required
    def get(self, id):
        """List all items"""
        user_id = get_jwt_identity()
        bucket = Bucket.find(id, user_id)
        if bucket:
            return bucket.items, 200
        else:
            return {"message": "You do not own a bucketlist with id {0}".format(id)}, 404

    @ns.doc('create_items')
    @ns.expect(item)
    @jwt_required
    def post(self, id):
        """Create a new item"""
        if not api.payload:
            return {"message": "Payload missing"}, 400  # Bad request

        data = api.payload.keys()
        if 'name' in data:
            user_id = get_jwt_identity()
            buck = Bucket.find(id, user_id)
            if buck:
                api.payload.update({'bucket_id': id})
                item_exists = Item.where(name=api.payload['name'].strip(), bucket_id=id).first()

                if item_exists:
                    return {'message': 'Item name already used in this bucket. Choose a different name to add an item'}, 406

                itm = Item(api.payload)
                itm.store()
                return {'message': 'Added item to bucket {0}'.format(id)}, 201
            else:
                return {'message': 'You do not own a bucket with id {0}'.format(id)}, 403  # Forbidden
        else:
            return {'message': 'Item name is required'}, 400  # Bad request


@ns.route('/bucketlists/<int:id>/items/<int:item_id>')
@ns.response(200, 'Item found')
@ns.param('id', 'The Bucket identifier')
@ns.param('item_id', 'The Item identifier')
class Items(Resource):
    """Show a single bucket item and lets you update or delete them"""
    @ns.doc('get_bucket_item')
    @ns.marshal_with(item)
    @jwt_required
    def get(self, id, item_id):
        """Fetch a given bucket"""
        user_id = get_jwt_identity()
        buck = Bucket.find(id, user_id)
        if buck:
            itm = Item.where(id=item_id, bucket_id=id).first()
            return itm, 200
        else:
            return {"message": "You do not own a bucketlist with id {0}".format(id)}, 404

    @ns.doc('delete_backet_item')
    @ns.response(204, 'Item deleted')
    @jwt_required
    def delete(self, id, item_id):
        """Delete a bucket given its identifier"""
        user_id = get_jwt_identity()
        buck = Bucket.find(id, user_id)
        if buck:
            itm = Item.where(id=item_id, bucket_id=id).first()
            if itm:
                itm.delete()
                return {'message': 'Item deleted'}, 204
            else:
                return {'message': 'Item not found'}, 404
        else:
            return {"message": "You do not own a bucketlist with id {0}".format(id)}, 404


    @ns.expect(bucket)
    @ns.marshal_with(bucket)
    @jwt_required
    def put(self, id, item_id):
        """Update an Item given a bucket identifier and Item identifier"""
        if not api.payload:
            return {"message": "Payload missing"}, 400  # Bad request

        data = api.payload.keys()
        if 'name' in data:
            user_id = get_jwt_identity()
            buck = Bucket.find(id, user_id)
            if not buck:
                return {"message": "You do not own a bucketlist with id {0}".format(id)}, 404

            itm = Item.where(id=item_id, bucket_id=id).first()

            # Check if there are changes
            if itm.name == api.payload['name']:
                return {'message': 'Item name has not changed, update not allowed'}, 406  # Not allowed

            if itm:
                itm.put(api.payload)
                return itm, 200
            else:
                return {'message': 'Item not found'}, 404
        else:
            return {'message': 'Item name is required'}, 400  # Bad request

# App launcher
app.run()