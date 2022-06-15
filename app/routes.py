import flask
from flask import session, request, redirect, render_template, url_for
from flask_user import login_required, UserManager, UserMixin
from app import app, user_manager

@app.route("/")
def hello():
    return 'hello'


@app.route("/finish")
@login_required
def finish():
    return 'finish!'

