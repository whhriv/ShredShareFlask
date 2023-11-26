import os
basedir = os.path.abspath(os.path.dirname(__file__))
# DATABASE_URL=postgresql://ogaasqnh:NExVeeCUSjCx09mRBfOukSovv7IotUbT@mahmud.db.elephantsql.com/ogaasqnh
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False