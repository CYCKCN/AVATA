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
    # print(current_user.email)
    # print(roomInfo_book)
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
    if room_id == "search": return redirect(url_for('user.search'))
    room = roomdb.db.find_one({"roomName": room_id})
    print(room_id)
    roomName = room['roomName']
    roomLoc = room['roomLoc']
    if request.method == "POST":
        # CURRENT_ROOM(room_id=room_id)
        if request.form.get('enter'):
            accountdb.updateRoom(current_user.email, room_id)
            return redirect(url_for('user.device',room_id=current_user.room))
        elif request.form.get('book'):
            accountdb.updateRoom(current_user.email, room_id)
            return redirect(url_for('user.booking',room_name=current_user.room))
    
    return render_template('room.html', room_id=roomName, room_loc=roomLoc)

@user.route("/device/<room_id>", methods=['POST','GET'])
@check_login
def device(room_id):
    img = url_for('static',filename='images/test/'+room_id+'/360-1.jpg')
    # image = cv2.imread(img)
    # V, U, _ = image.shape
    # print(V, U)

    dic = devicedb.checkDeviceList(room_id, 1002, 2014) # should be shape of 360 image
    # print(current_user.room)
    # print(current_user.email)
    # print(dic)
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
@check_login
def booking(room_name):
    # return "In Progress"
    today_date = get_today_date()
    time_list = [t[:2] + ' : ' + t[2:] for t in time]
    week, access_date = get_booking_week()
    month = MONTH_ABBR[today_date[1]]
    year = today_date[0]
    occupy = roomdb.checkRoomAvailable(room_name, extend_access_date=access_date, get_occupy=True)
    # print(occupy)

    if request.method == "POST":
        if request.form.get('back'):
            return redirect(url_for('user.room', room_id=room_name))
        elif request.form.get('home'):
            return redirect(url_for('user.search'))
        elif request.form.get('confirm'):
            # CURRENT_ROOM.get_booking_result()
            booking_period = []
            myself=request.form.get(f'myself')
            guest=request.form.get(f'guest')
            guestemail=request.form.get('guestemail')
            for k, v in occupy.items():
                t,d=k
                if v=='y': continue
                if request.form.get(f"time-{d}-{t}"):
                    time_data="{:d}/{:0>2d}/{:0>2d}".format(today_date[0],today_date[1],d)
                    clock=t.replace(' : ','')
                    booking_period.append(clock)
            booking_period.append(time[time.index(booking_period[-1]) + 1])
            roomdb.setRoomBookByUser(room_name, time_data, current_user.email, booking_period[0], booking_period[-1])
                    # self.db_bookroom(self.db['rooms'],self.db_roomone['_id'],time_data,clock)
            return redirect(url_for('user.room',room_id=room_name))
        elif request.form.get('delete'):
            pass
    
    return render_template('booking.html', room_id=room_name,time=time_list,week=week,month=month,year=year,occupy=occupy)

@user.route("/initial", methods=['POST','GET'])
def initial():
    # print("initial")
    # print(current_user.room)
    # print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    # print(steps)
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
    # print("turnon")
    # print(current_user.room)
    # print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    # print(steps)
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
    # print("pair")
    # print(current_user.room)
    # print(current_user.email)
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
    # print("zoom")
    # print(current_user.room)
    # print(current_user.email)
    steps = roomdb.checkInsInitialStepList(current_user.room)
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('user.search'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('user.pair'))
    
    return render_template('instruction_zoom.html',room_id=current_user.room,steps=steps)