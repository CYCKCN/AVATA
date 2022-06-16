import secrets

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

    USER_LOGIN_TEMPLATE = 'login.html'
    USER_REGISTER_TEMPLATE = 'register.html'


from app import db
from flask_user import UserMixin

class User(db.Document, UserMixin):
    meta = {'collection':'accounts'}

    username = db.StringField(default='', required=True)
    password = db.StringField(required=True)

    email = db.StringField(default='', required=True)
    room = db.StringField(default='', required=True)

    roles = db.StringField(default='USER', required=True)


from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import InputRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    username = wtforms.StringField('username', validators=[InputRequired(), Length(max=10)])
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])
    passwordRepeat = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    room = wtforms.StringField('room', validators=[InputRequired(), Length(max=30)])

    roles = wtforms.RadioField('roles', validators=[InputRequired()], choices=[('USER', 'User'), ('ADMIN', 'Admin')])


class LoginForm(FlaskForm):
    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

class RoomBasicForm(FlaskForm):
    roomName = wtforms.StringField('roomName', validators=[InputRequired(), Length(max=10)])
    roomImage = wtforms.FileField('roomImage', validators=[InputRequired(), Regexp('([^\\s]+(\\.(?i)(jpe?g|png|bmp))$)')])
    roomLoc = wtforms.StringField('roomLoc', validators=[InputRequired(), Length(max=30)])
