from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request
from flask_user import login_required
from .models import RegisterForm, LoginForm, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import user_manager
from flask_login import login_user, logout_user, current_user

# Don't use @login_required, it will lead to strange problems...
# Use
# if not current_user.is_authenticated: return redirect(url_for('authen.login'))
# Or use:
# @check_login
# -by shaun

def check_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated: 
            return redirect(url_for('authen.login'))
        return f(*args, **kwargs)
    return wrapper

authen_blue=Blueprint('authen',__name__,url_prefix='/authen')

@authen_blue.route('/')
def main():
    return 'authentic'

@authen_blue.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('authen.secret'))

    form=LoginForm()
    if request.method=='POST':
        if form.validate():
            email=form.email.data
            password=form.password.data

            exist=User.objects(email=email).first()
            if exist:
                if check_password_hash(exist['password'], password):
                    login_user(exist)
                    if exist['roles']=='ADMIN':
                        return redirect(url_for('admin.main'))
                    else:
                        return redirect(url_for('authen.secret'))
                else:
                    return render_template('login.html', form=form, pass_right=False, register=False)
            else:
                return render_template('login.html', form=form, pass_right=True, register=True)

    return render_template('login.html', form=form, pass_right=True, register=False)

@authen_blue.route('/register', methods=['POST','GET'])
def register():
    form=RegisterForm()
    if request.method=='POST':
        if form.validate():
            username=form.username.data
            email=form.email.data
            room=form.room.data
            password=form.password.data
            roles=form.roles.data
            
            exist=User.objects(email=email).first()
            if exist is None:
                hashpassword=generate_password_hash(password, method='sha256')
                user=User(username=username, password=hashpassword, email=email, room=room, roles=roles).save()
                login_user(user)
                #return form.username.data+' '+form.email.data+' '+form.room.data+' '+form.password.data+' '+form.roles.data
                return redirect(url_for('authen.secret'))
            else:
                return render_template('register.html', form=form, exist=True)
                

    return render_template('register.html', form=form, exist=False)

@authen_blue.route('/logout')
@check_login
def logout():
    logout_user()
    return redirect(url_for('authen.login'))

@authen_blue.route('/change-password', methods=['POST','GET'])
@check_login
def reset():
    if request.method=="POST":
        return ''
    return render_template('reset.html')

'''
@authen_blue.route('/secret', methods=['POST','GET'])
@check_login
def secret():
    if request.method=='POST':
        return redirect(url_for('hello'))
    return 'secret page'
'''