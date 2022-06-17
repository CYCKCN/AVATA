import os
from flask import Blueprint, render_template, redirect, url_for, request
from .authen import check_login
from .img_trans import *

admin_blue=Blueprint('admin',__name__,url_prefix='/admin')

@admin_blue.route('/')
def enter():
    return 'admin flow'

@admin_blue.route("/logout", methods=['GET'])
def logout():  
    return render_template('admin_logout.html')

@admin_blue.route("/login", methods=['POST','GET'])
def login():
    #plz use /authen/login to login to /admin/main -by shaun
    #you can register a admin account to access /admin/main
    if request.method == "POST":
        text = request.form.get('email')
        password = request.form.get('pwd')
        if text or password:
            return redirect(url_for('admin.main'))
    
    return render_template('admin_login.html')

@admin_blue.route("/main", methods=['POST','GET'])
@check_login #plz use wrapper function @check_login where you want user to login
def main():
    roomInfo={
        0:{'name':'5554','lift':'27-28','date':'August 21','time':'19:00-21:00'},
        1:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        2:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        3:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        4:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        5:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        6:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
    }

    if request.method == "POST":
        room_id=request.form.get('roomid')
        add=request.form.get('add')
        if add:
            return redirect(url_for('admin.basic_info'))
        if room_id:
            return redirect(url_for('admin.room',room_id=room_id))
    
    return render_template('admin_main.html',roomInfo=roomInfo)

@admin_blue.route("/room/<room_id>", methods=['POST','GET'])
@check_login 
def room(room_id):
    if request.method == "POST":
        edit=request.form.get('edit')
        if edit:
            return redirect(url_for('admin.basic_info',room_id=room_id))
        delete=request.form.get('delete')
        if delete:
            return redirect(url_for('admin.main'))
    
    return render_template('admin_room.html',room_id=room_id)

@admin_blue.route("/basic_info", methods=['POST','GET'])
def basic_info():
    room_id = request.args.get('room_id')
    if request.method == "POST":
        continue_=request.form.get('continue')
        img_base64=request.form.get('imgSrc')
        image_decoder((img_base64.split(','))[-1],
        f'app/static/images/test/room{room_id}/_basic_upload.png')
        if continue_:
            return redirect(url_for('admin.photo_360',room_id=room_id))
    
    return render_template('admin_basic_info.html',room_id=room_id)

@admin_blue.route("/photo_360", methods=['POST','GET'])
def photo_360():
    room_id = request.args.get('room_id')
    if request.method == "POST":
        continue_=request.form.get('continue')
        img360_base64=request.form.get('img360Src')
        #rint(img360_base64)
        if continue_:
            return redirect(url_for('admin.device_info',room_id=room_id))
    
    return render_template('admin_360_photo.html',room_id=room_id)


devices_dict = {}
from objects_admin import *

@admin_blue.route("/device_info", methods=['POST','GET'])
def device_info():
    room_id = request.args.get('room_id')
    
    global devices_test_admin  # Three point initalization
    devices_dict[room_id] = devices_test_admin

    if request.method == "POST":
        continue_=request.form.get('continue')
        checklist=request.form.get('checkList')
        if continue_:
            return redirect(url_for('admin.instruction_pair',room_id=room_id))
        if checklist:
            return redirect(url_for('admin.device_list',room_id=room_id))

        update_from_admin_request(devices_dict[room_id])
    
    return render_template('admin_device_info.html',room_id=room_id,devices=devices_dict[room_id].getJson(),devices_choose=devices_dict[room_id].chooseDevice())

@admin_blue.route("/device_list", methods=['GET'])
def device_list():
    room_id = request.args.get('room_id')
    return render_template('admin_device_list.html',room_id=room_id,devices=devices_dict[room_id].getJson())


@admin_blue.route("/instruction_pair", methods=['POST','GET'])
def instruction_pair():
    room_id = request.args.get('room_id')
    if request.method == "POST":
        pass
    
    return render_template('admin_device_info.html',room_id=room_id)
