from flask import Blueprint

user_blue=Blueprint('user',__name__)

@user_blue.route('/')
def main():
    return 'user flow'

