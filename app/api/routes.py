from . import api
from app import db
from app.models import  Skis, Surf, User
from flask import Flask, request
from flask_cors import cross_origin
from flask import Flask, jsonify


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

@api.route('/users', methods=['POST'])
def create_user():

    data = request.json
    new_user = User(username=data['username'], location=data['location'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})




from . import routes 