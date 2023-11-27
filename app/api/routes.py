from . import api
from app import db
from app.models import  Skis, Surf, User
from flask import Flask, request, url_for
from flask_cors import cross_origin
from flask import Flask, jsonify
from app.api.errors import bad_request
from .auth import basic_auth, token_auth


@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token}

@api.route('/skis')
@cross_origin()
def get_skis():
    skis = db.session.execute(db.select(Skis)).scalars().all()
    return [ski.to_dict() for ski in skis]

@api.route('/surf')
def get_surf():
    surf = db.session.execute(db.select(Surf)).scalars().all()
    return [surf.to_dict() for surf in surf]

@api.route('/users', methods=['POST','GET'])
# @cross_origin()
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.to_dict() for user in users]

# @api.route('/users', methods=['POST'])
# @cross_origin()
# def create_user():

#     data = request.json
#     new_user = User(username=data['username'], location=data['location'], email=data['email'], password=data['password'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'})

# @api.route('/users', methods=['POST'])
# @cross_origin()
# def create_user():
#     print(request.get_json())
#     data = request.get_json() or {}
#     if 'username' not in data or 'email' not in data or 'password' not in data:
#         return bad_request('must include username, email and password fields')
#     if User.query.filter_by(username=data['username']).first():
#         return bad_request('please use a different username')
#     if User.query.filter_by(email=data['email']).first():
#         return bad_request('please use a different email address')
#     user = User()
#     print(data)
#     user.from_dict(data, new_user=True)
#     db.session.add(user)
#     db.session.commit()
#     print('we are in the route')
#     response = jsonify(user.to_dict())
#     response.status_code = 201
#     response.headers['Location'] = url_for('api.get_user', id=user.id)
#     return response

# Endpoing to create a new User
# @api.route('/users', methods=['POST'])
# @cross_origin()
# def create_user():
#     # Check to see that the request body is JSON
#     if not request.is_json:
#         return {'error': 'Your content-type must be application/json'}, 400
    
#     # Get the data from the request body
#     data = request.json

#     # Check to see if all of the required fiels are present
#     required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
#     missing_fields = []
#     for field in required_fields:
#         if field not in data:
#             missing_fields.append(field)
#     if missing_fields:
#         return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
#     # Get the values from the data
#     # first_name = data.get('firstName')
#     # last_name = data.get('lastName')
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
    
#     # Check if there is already a user with username or email
#     check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
#     if check_user:
#         return {'error': 'A user with that username and/or email already exists'}, 400
    
#     # Create a new user
#     new_user = User(username=username, email=email, password=password)
#     # Add to the database
#     db.session.add(new_user)
#     db.session.commit()
#     # return the dictionary/JSON version of the user
#     return new_user.to_dict(), 201


# # Endpoint to get user based on token
# @api.route('/users/<int:id>', methods=["GET"])
# @cross_origin()
# @token_auth.login_required
# def get_user(id):
#     current_user = token_auth.current_user(id)
#     return current_user.to_dict()

# @api.route('/users', methods=['GET'])
# @token_auth.login_required
# @cross_origin()
# def get_users():
#     users = db.session.execute(db.select(User)).scalars().all()
#     return [user.to_dict() for user in users]

# # Endpoint to edit an exiting user
# @api.route('/users/<user_id>', methods=['PUT'])
# @token_auth.login_required
# @cross_origin()
# def edit_user(user_id):
#     # Check to see that the request body is JSON
#     if not request.is_json:
#         return {'error': 'Your content-type must be application/json'}, 400
#     # Get the post from db
#     user = db.session.get(User, user_id)
#     if user is None:
#         return {'error': f"User with an ID of {user_id} does not exist"}, 404
#     data = request.json
#     for field in data:
#         if field in {'username', 'email'}:
#             setattr(user, field, data[field])
#     db.session.commit()
#     return user.to_dict()

# # Endpoint to delete an exiting user
# @api.route('/users/<user_id>', methods=["DELETE"])
# @token_auth.login_required
# @cross_origin()
# def delete_user(user_id):
#     # Get the user from db
#     user = db.session.get(User, user_id)
#     # Delete the user
#     db.session.delete(user)
#     db.session.commit()
#     return {'success': f"{user.username} has been deleted"}


from . import routes 