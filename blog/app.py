import re
from flask import Flask
from blog.models import db, User
from blog.config import configs
from flask_migrate import Migrate
from flask_login import LoginManager


def register_extentions(app):
    db.init_app(app)
    Migrate(app,db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

def register_blueprints(app):
    from .handlers import front,admin
    app.register_blueprint(front)
    app.register_blueprint(admin)

    
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
     
    register_extentions(app)
    register_blueprints(app)
    app.add_template_filter(isOdd,'isOdd')
    app.add_template_filter(splitTag,'splitTag')
    
    return app

def isOdd(value):
    if int(value[-1])%2==0:
        return False
    else:
        return True

def splitTag(values):
    return re.split('[,，]', values)
