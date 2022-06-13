from flask import Blueprint

user_blue=Blueprint('user',__name__,url_prefix='/user')

@user_blue.route('/')
def main():
    return 'user flow'

