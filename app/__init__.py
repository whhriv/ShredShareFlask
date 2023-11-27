from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login = LoginManager(app)
login.login_view = 'login'

from app.api import api #as api_bp
app.register_blueprint(api)

# def create_app(config_class=Config):


#     from app.api import api as api_bp
#     app.register_blueprint(api_bp, url_prefix='/api')
    



from app import routes, models