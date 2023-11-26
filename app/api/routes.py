from . import api
from app import db
from app.models import  Skis, Surf, User



@api.route('/skis')
def get_skis():
    skis = db.session.execute(db.select(Skis)).scalars().all()
    return [ski.to_dict() for ski in skis]

@api.route('/surf')
def get_surf():
    surf = db.session.execute(db.select(Surf)).scalars().all()
    return [surf.to_dict() for surf in surf]

@api.route('/users')
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.to_dict() for user in users]



from . import routes 