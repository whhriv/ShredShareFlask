from . import api
from app import db
from app.models import  Skis, Surf, User
from flask import Flask, request, url_for, redirect
from flask_cors import cross_origin, CORS
from flask import Flask, jsonify
from app.api.errors import bad_request
from .auth import basic_auth, token_auth
from app.forms import RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from ..forms import LoginForm, EditProfileForm, PostForm, SkiForm, SurfForm, UserForm


app = Flask(__name__)
CORS(app)
CORS(api)


# @api.route('/token')
# @basic_auth.login_required
# def get_token():
#     auth_user = basic_auth.current_user()
#     token = auth_user.get_token()
#     return {'token': token}

@api.route('/users/me', methods=["GET"])
@token_auth.login_required
def get_me():
    current_user = token_auth.current_user()
    return current_user.to_dict()


@api.route('/skis')
# @cross_origin()
def get_skis():
    skis = db.session.execute(db.select(Skis)).scalars().all()
    return [ski.to_dict() for ski in skis]


@api.route('/createskis', methods=['POST'])
@cross_origin()
@token_auth.login_required
def create_ski():
    data = request.json
    user_id = current_user.id if current_user.is_authenticated else None
    print('user_id',user_id)
    new_ski = Skis(
        title=data['title'], 
        length=data['length'], 
        make=data['make'], 
        model=data['model'],
        binding=data['binding'], 
        description=data['description'],
        # image_url=data.get('imageUrl', None),
        user_id=user_id
        )
    db.session.add(new_ski)
    db.session.commit()
    return new_ski.to_dict(), 201

# @api.route('/editskis/<ski_id>', methods=['PUT'])
# @token_auth.login_required
# def edit_ski(ski_id):
#     if not request.is_json:
#         return {'error': 'Your content-type must be application/json'}, 400
#     ski = db.session.get(Skis, ski_id)
#     if ski is None:
#         return {'error': f"ski with an ID of {ski_id} does not exist"}, 404
#     current_user = token_auth.current_user()
#     if ski.author != current_user:
#         return {'error': 'You do not have permission to edit this ski'}, 403
#     data = request.json
#     for field in data:
#         if field in {'title', 'body', 'imageUrl'}:
#             if field == 'imageUrl':
#                 setattr(ski, 'image_url', data[field])
#             else:
#                 setattr(ski, field, data[field])
#     db.session.commit()
#     return ski.to_dict()

# @api.route('/deleteskis/<ski_id>', methods=["DELETE"])
# @token_auth.login_required
# def delete_ski(ski_id):
#     ski = db.session.get(Skis, ski_id)
#     if ski is None:
#         return {'error': f'ski with an ID of {ski_id} does not exist'}, 404
#     current_user = token_auth.current_user()
#     if ski.author != current_user:
#         return {'error': 'You do not have permission to delete this ski'}, 403
#     db.session.delete(ski)
#     db.session.commit()
#     return {'success': f"{ski.title} has been deleted"}

@api.route('/surf')
def get_surf():
    surf = db.session.execute(db.select(Surf)).scalars().all()
    return [surf.to_dict() for surf in surf]

@api.route('/createsurf', methods=['POST'])
@cross_origin()
# @token_auth.login_required
def create_surf():
    data = request.json
    new_surf= Surf(
        title=data['title'], 
        length=data['length'], 
        make=data['make'], 
        model=data['model'],
        description=data['description'],
        # image_url=data.get('imageUrl', None),
        user_id=1 #current_user.id
        )
     # user_id=current_user.get_id()
    db.session.add(new_surf)
    db.session.commit()
    return new_surf.to_dict(), 201

@api.route('/surf/edit/<surf_id>', methods=["GET", "POST"])
@login_required
def edit_surf(surf_id):
    surf = db.session.get(Surf, surf_id)
    if not surf:
        print('That post does not exist')
        return redirect(url_for('edit_skis'))
    if current_user != surf.user_id:
        print('You can only edit skis you have authored!')
        # return redirect(url_for('edit_skis.html', ski_id=ski_id))
    # Create an instance of the SkiForm
    form = SurfForm()

    # If form submitted, update the post
    if form.validate_on_submit():
        # update the post with the for data
        surf.title = form.title.data
        surf.description = form.description.data
        surf.length=form.length.data,
        surf.make=form.make.data,
        surf.model=form.model.data,
        surf.description=form.description.data,
        surf.user_id=current_user.id
        # surf.image_url = form.image_url.data
        # Commit to the database
        db.session.commit()
        print(f'{surf.title} has been edited.', 'success')
        return redirect(url_for('surf'))
    form.title.data = surf.title
    form.description.data = surf.description
    form.length.data = surf.length
    form.make.data = surf.make
    form.model.data = surf.model
    
    # form.image_url.data = surf.image_url
    return form

@api.route('/surf/<surf_id>', methods=['PUT'])
@token_auth.login_required
def edit_ski(surf_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    surf = db.session.get(Surf, surf_id)
    if surf is None:
        return {'error': f"surf with an ID of {surf_id} does not exist"}, 404
    current_user = token_auth.current_user()
    if surf.author != current_user:
        return {'error': 'You do not have permission to edit this surf'}, 403
    data = request.json
    for field in data:
        if field in {'title', 'body', 'imageUrl'}:
            if field == 'imageUrl':
                setattr(surf, 'image_url', data[field])
            else:
                setattr(surf, field, data[field])
    db.session.commit()
    return surf.to_dict()

@api.route('/surf/<surf_id>', methods=["DELETE"])
@token_auth.login_required
def delete_ski(surf_id):
    surf = db.session.get(Surf, surf_id)
    if surf is None:
        return {'error': f'surf with an ID of {surf_id} does not exist'}, 404
    current_user = token_auth.current_user()
    if surf.author != current_user:
        return {'error': 'You do not have permission to delete this surf'}, 403
    db.session.delete(surf)
    db.session.commit()
    return {'success': f"{surf.title} has been deleted"}

@api.route('/users', methods=['POST','GET']) #token authentication for GET
# @cross_origin()
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.to_dict() for user in users]

@api.route('/login', methods=['POST', 'GET']) #removed 'GET' #token authentication for GET
@cross_origin()
def login_user():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            print('Invalid username or password', 'error')
       

    return jsonify({'message': 'Login successful'}), 200


    

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