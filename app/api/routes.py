from . import api
from app import db
from app.models import  Skis, Surf, User
from flask import Flask, request, url_for
from flask_cors import cross_origin, CORS
from flask import Flask, jsonify
from app.api.errors import bad_request
from .auth import basic_auth, token_auth
from app.forms import RegistrationForm


CORS(api)


@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token}

@api.route('/skis')
# @cross_origin()
def get_skis():
    skis = db.session.execute(db.select(Skis)).scalars().all()
    return [ski.to_dict() for ski in skis]

# @api.route('/skis/<ski_id>')
# # @cross_origin()
# def get_skis(id):
#     ski = db.session.get(Skis, id)
#     if not ski:
#         return {'Ski with ID of {ski_id} does not exist'}, 404
#     return ski.to_dict()

@api.route('/createskis', methods=['POST'])
@cross_origin()
def create_ski():
    data = request.json
    new_ski = Skis(
        title=data['title'], 
        length=data['length'], 
        make=data['make'], 
        model=data['model'],
        binding=data['binding'], 
        description=data['description'],
        # image_url=data.get('imageUrl', None),
        user_id=1
        )
    db.session.add(new_ski)
    db.session.commit()
    return new_ski.to_dict(), 201

@api.route('/surf')
def get_surf():
    surf = db.session.execute(db.select(Surf)).scalars().all()
    return [surf.to_dict() for surf in surf]

@api.route('/createsurf', methods=['POST'])
@cross_origin()
def create_surf():
    data = request.json
    new_surf= Surf(
        title=data['title'], 
        length=data['length'], 
        make=data['make'], 
        model=data['model'],
        description=data['description'],
        # image_url=data.get('imageUrl', None),
        user_id=1
        )
     # user_id=current_user.get_id()
    db.session.add(new_surf)
    db.session.commit()
    return new_surf.to_dict(), 201

@api.route('/users', methods=['POST','GET']) #token authentication for GET
# @cross_origin()
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.to_dict() for user in users]

@api.route('/register', methods=['POST', 'GET'])
@cross_origin()
def create_user():


    data = request.json
    new_user = User(username=data['username'], location=data['location'],  email=data['email'], password_hash=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict(), 201
    # return jsonify({'message': 'User created successfully'})


    

from . import routes 