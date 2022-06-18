import flask
import secrets
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_user import UserManager, UserMixin

'''
print("##")
from .models import ConfigClass
print("##")
'''
class ConfigClass(object):
    SECRET_KEY = secrets.token_hex(16)

    MONGODB_SETTINGS = {
        'db': 'AVATA',
        'host': 'mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/AVATA?retryWrites=true&w=majority'
    }

    USER_APP_NAME = "AVATA" 
    USER_ENABLE_EMAIL = False     
    USER_ENABLE_USERNAME = True  
    USER_REQUIRE_RETYPE_PASSWORD = False  

    #USER_LOGIN_TEMPLATE = 'login.html'
    #USER_REGISTER_TEMPLATE = 'register.html'

    #USER_LOGIN_URL = '/authen/login'
    #USER_REGISTER_URL = '/authen/register'

    #USER_UNAUTHENTICATED_ENDPOINT = 'authen.login'

app = Flask(__name__)
app.config.from_object(ConfigClass)

mongo = MongoEngine(app)

from .models import User

user_manager = UserManager(app, mongo, User)

from .database import connection, AccountDB, DeviceDB, RoomDB

db = connection("AVATA")
accountdb = AccountDB(db)
devicedb = DeviceDB(db)
roomdb = RoomDB(db)

from app import routes
from .user import user_blue
from .admin import admin_blue
from .authen import authen_blue

app.register_blueprint(user_blue)
app.register_blueprint(admin_blue)
app.register_blueprint(authen_blue)
