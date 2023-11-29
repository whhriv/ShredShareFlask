from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask import url_for


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page, error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            # '_meta': {
            #     'page': page,
            #     'per_page': per_page,
            #     'total_pages': resources.pages,
            #     'total_items': resources.total
            # },
            # '_links': {
            #     'self': url_for(endpoint, page=page, per_page=per_page,**kwargs),
            #     'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
            #     'prev': url_for(endpoint, page=page - 1, per_page=per_page,**kwargs) if resources.has_prev else None
            # }
        }
        return data

class User(db.Model, UserMixin, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(64), index=True, unique=True)
    about_me = db.Column(db.String(140), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'location': self.location,
            'about_me': self.about_me,
            # 'ski_count': Skis.count(), #?????
            # 'follower_count': self.followers.count(),
            # 'followed_count': self.followed.count(),
            # '_links': {
            #     'self': url_for('api.get_user', id=self.id),
            #     'followers': url_for('api.get_followers', id=self.id),
            #     'followed': url_for('api.get_followed', id=self.id),
                # 'avatar': self.avatar(128)
            # }
        }
        if include_email:
            data['email'] = self.email
        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
class Skis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    length = db.Column(db.String, nullable=False)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    binding = db.Column(db.String, nullable=False, default='')
    description = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # image_url = db.Column(db.String, nullable=True )

    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'length': self.length,
            'make': self.make,
            'model': self.model,
            'binding': self.binding,
            'description': self.description,
            'dateCreated': self.date_created,
            'userId': self.user_id,
            # 'imageUrl': self.image_url,
            
        }

class Surf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    length = db.Column(db.String, nullable=False)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #image_url = db.Column(db.String, default=random_photo)

    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def to_dict(self):
        return {
            'surf_id': self.id,
            'title': self.title,
            'length': self.length,
            'make': self.make,
            'model': self.model,
            'description': self.description,
            'length': self.length,
            'dateCreated': self.date_created,
            'userId': self.user_id,
            # 'imageUrl': self.image_url,
            # 'author': self.author.to_dict()
        }
    

