import os
import cv2
from flask import Flask
from flask import Blueprint, request, redirect, url_for, render_template

from .auth import check_login
from .database.db import accountdb, devicedb, roomdb
from .database.object import PERSONAL_TYPE, get_today_date, time, MONTH_ABBR, get_booking_week
from flask_login import current_user

# from test_data import ROOM, MONTH_ABBR

user = Blueprint('user', __name__)
# CURRENT_ROOM=ROOM(oscwd=os.getcwd())

@user.route('/', methods=['POST', 'GET'])
@check_login
def main():
    return redirect(url_for('user.search'))

@user.route("/search", methods=['POST','GET'])
@check_login
def search():
    room_id = ''
    roomInfo_book = roomdb.checkUserBooking(current_user.email)
    print(current_user.email)
    print(roomInfo_book)
    roomInfo_result = {}
    # account = accountdb.findUser(current_user.get_id)
    if request.method == "POST":
        room_id = request.form.get('room_id') 
        btn_search=request.form.get('btn_search')
        timetable=request.form.get('timetable')
        btn_profile=request.form.get('profile')

        # roomInfo_result = roomdb.checkSearchRoom(room_id, current_user.email)
        # return render_template('search.html', room_id=room_id, roomInfo_book=roomInfo_book, roomInfo_result=roomInfo_result)
        if btn_profile and room_id=='':
            return redirect(url_for('user.profile'))
        if room_id:
            return redirect(url_for('user.room', room_id="5554")) 
        # print(btn_search)
        # if btn_search:
        #     return redirect(url_for('search'))
        #     roomInfo_result = roomdb.checkSearchRoom(room_id, current_user.email)
        #     return render_template('search.html', room_id=room_id, roomInfo_book=roomInfo_book, roomInfo_result=roomInfo_result)

    return render_template('search.html', room_id=room_id, roomInfo_book=roomInfo_book, roomInfo_result=roomInfo_result)

@user.route("/room/<room_id>", methods=['POST','GET'])
@check_login
def room(room_id):
    if request.method == "POST":
        # CURRENT_ROOM(room_id=room_id)
        if request.form.get('enter'):
            accountdb.updateRoom(current_user.email, room_id)
            return redirect(url_for('user.device',room_id=current_user.room))
        elif request.form.get('book'):
            accountdb.updateRoom(current_user.email, room_id)
            return redirect(url_for('user.booking',room_name=current_user.room))
    
    return render_template('room.html')

@user.route("/device/<room_id>", methods=['POST','GET'])
@check_login
def device(room_id):
    img = url_for('static',filename='images/test/'+room_id+'/360-1.jpg')
    # image = cv2.imread(img)
    # V, U, _ = image.shape
    # print(V, U)

    dic = devicedb.checkDeviceList(room_id, 1002, 2014)
    print(current_user.room)
    print(current_user.email)
    print(dic)
    for i, d in dic.items():
        print(d['name'], d['u'], d['v'])
    if request.method == "POST":
        personal = request.form.get('personal')
        confirm = request.form.get('confirm')  # how to run confirm button

        if personal:
            # CURRENT_ROOM.get_data_choose_devices()
            # CURRENT_ROOM.get_data_personal_device(device)
            for d in PERSONAL_TYPE:
                if request.form.get(d):
                    accountdb.updatePersonal(current_user.email, d)
            print(current_user.personal)
            # CURRENT_ROOM.set_data_instruction()
        if confirm:
            dev = []
            for i, d in dic.items():
                if request.form.get(d['name']):
                    dev.append(d['name'])
            accountdb.updateDevice(current_user.email, dev)
            print(current_user.dev)
            return redirect(url_for('user.initial'))

    
    # dic=CURRENT_ROOM.set_data_choose_devices(use_related=True)
    
    #print(dic)
    return render_template('device.html', dic=dic, img=img)

@user.route("/booking/<room_name>", methods=['POST','GET'])
def booking(room_name):
    return "In Progress"
    # if request.method == "POST":
    #     if request.form.get('back'):
    #         return redirect(url_for('user.room', room_id=room_name))
    #     elif request.form.get('home'):
    #         return render_template('search.html', room_id=room_name)
    #     elif request.form.get('book'):
    #         CURRENT_ROOM.get_booking_result()
    #         return redirect(url_for('user.room',room_id=room_name))

    # today_date = get_today_date()
    # time_list = [t[:2] + ' : ' + t[2:] for t in time]
    # week = get_booking_week()
    # month = MONTH_ABBR[today_date[1]]
    # year = today_date[0]
    # roomdb.setRoomBookByUser(room_name, )

    # for t in time:
    #     for d in self.booking_access_date:
    #         _t=t[:2]+' : '+t[2:]
    #         _d=int(d.split('/')[2])
    #         if not day.get(d) is None and t in day[d]:
    #             occupy[(_t,_d)]='y'
    #         else:
    #             occupy[(_t,_d)]='n'

    # occupy=CURRENT_ROOM.set_booking_occupy()
    # return render_template('booking.html', room=room_name,time=time_list,week=week,month=month,year=year,occupy=occupy)

# @user.route("/personal-device", methods=['POST','GET'])
# def personal_device():
#     if request.method == "POST":
#         device=[]
#         for d in PERSONAL_TYPE:
#             if request.form.get(d):
#                 device.append(d)

#         #global CURRENT_ROOM
#         CURRENT_ROOM.get_data_personal_device(device)
#         CURRENT_ROOM.set_data_instruction()

#         return redirect(url_for('device',room_id=CURRENT_ROOM.room_id))

#     return render_template('personal-device.html')

# @user.route("/instruction-choose", methods=['POST','GET'])
# def instructor_choose():
#     #global CURRENT_ROOM
#     if request.method == "POST":
#         device=request.form.get('input')
#         CURRENT_ROOM.create_guide_queue(device)
#         return redirect(url_for('instruction'))
    
#     img=CURRENT_ROOM.image_360
#     dic=CURRENT_ROOM.choose_devices_relative(use_related=False)
#     order=CURRENT_ROOM.get_guide_order()
#     #pprint(dic)
#     #pprint(CURRENT_ROOM.image_360_deivces)
#     #pprint(CURRENT_ROOM.image_360_deivces_related)
#     return render_template('instruction-choose.html',dic=dic, image_path=img, order=order)

# @user.route("/instruction", methods=['POST','GET'])
# def instruction():
#     #global CURRENT_ROOM
#     guide=None
#     if request.method == "POST":
#         if len(CURRENT_ROOM.guide_queque)==0:
#             return redirect(url_for('instructor_choose'))
#         else:
#             guide=CURRENT_ROOM.pop_guide_queue()
#             return render_template('instruction.html',title="Guide of "+CURRENT_ROOM.guide_device,guide=guide)

#     guide=CURRENT_ROOM.pop_guide_queue()
#     return render_template('instruction.html',title="Guide of "+CURRENT_ROOM.guide_device,guide=guide)

# steps={
#    'step 1':{'text':'Find the HDMI cable underneath the conference table', 'image':'', 'command':"print('instruction_initial_list')\r\nprint(steps)", 'help':''},
#    'step 2':{'text':'Find the HDMI cable underneath the conference table', 'image':'8bdd60db4a154e428fd47f7d857b8cf9', 'command':"print('instruction_initial_list')\r\nprint(steps)", 'help':'helpxxxxxxxx xxxxxxxxxxxxxxx xxxxxxxxxxxx xxxxxxxxxxxx xxxxxxxxxxx'},
#    'step 3':{'text':'Plug the HDMI cable to your laptop', 'image':'8bdd60db4a154e428fd47f7d857b8cf9', 'command':'', 'help':''},
# }

@user.route("/initial", methods=['POST','GET'])
def initial():
    # print("initial")
    print(current_user.room)
    print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    print(steps)
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('user.turnon'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('user.device',room_id=current_user.room))
    
    return render_template('instruction_initial.html',room_id=current_user.room, steps=steps)

@user.route("/turnon", methods=['POST','GET'])
def turnon():
    print("turnon")
    print(current_user.room)
    print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    print(steps)
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('user.pair'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('user.initial'))
    
    return render_template('instruction_turnon.html', room_id=current_user.room, steps=steps)

@user.route("/pair", methods=['POST','GET'])
def pair():
    print("pair")
    print(current_user.room)
    print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('user.zoom'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('user.turnon'))
    
    return render_template('instruction_pair.html', room_id=current_user.room,steps=steps)

@user.route("/zoom", methods=['POST','GET'])
def zoom():
    print("zoom")
    print(current_user.room)
    print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('user.search'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('user.pair'))
    
    return render_template('instruction_zoom.html',room_id=current_user.room,steps=steps)

@user.route("/profile", methods=['POST','GET'])
def profile():
    if request.method == "POST":
        btn_profile=request.form.get('profile')
        if btn_profile:
            return redirect(url_for('user.search'))
        logout=request.form.get('logout')
        if logout:
            return redirect(url_for('admin.logout'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('user.search'))
    
    return render_template('user_profile.html')