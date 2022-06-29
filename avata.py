import os
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Flask
from easydict import EasyDict
from pprint import pprint

import demo_utils
from test_data import ROOM, PERSONAL_TYPE, MONTH_ABBR

PATH_templates='frontend/templates'
PATH_static='frontend/static'

app = Flask(__name__, template_folder=PATH_templates, static_folder=PATH_static)
#app = Flask(__name__)

CURRENT_ROOM=ROOM(oscwd=os.getcwd())

@app.route("/")
def hello():
    return 'hello'

roomInfo_recent={
        0:{'name':'5554','lift':'27-28','date':'August 21','time':'19:00-21:00'},
        1:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
    }

roomInfo_book={
        0:{'name':'5554','lift':'27-28','date':'August 21','time':'19:00-21:00'},
        1:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
    }

roomInfo_result={
        0:{'name':'5554','lift':'27-28','date':'August 21','time':'19:00-21:00'},
    }

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        if email:
            return redirect(url_for('search'))

    return render_template('login.html')

@app.route("/verification/<email>", methods=['POST','GET'])
def verification(email):
    if request.method == "POST":
        code = request.form.get('code')
        if code:
            return redirect(url_for('search'))

    return render_template('verification-code.html', userEmail=email)

@app.route("/device/<room_id>", methods=['POST','GET'])
def device(room_id):
    #global CURRENT_ROOM
    if request.method == "POST":
        personal = request.form.get('personal')
        confirm = request.form.get('confirm')  # how to run confirm button
        if personal:
            device=[]
            for d in PERSONAL_TYPE:
                if request.form.get(d):
                    device.append(d)

            CURRENT_ROOM.get_data_choose_devices()
            CURRENT_ROOM.get_data_personal_device(device)
            CURRENT_ROOM.set_data_instruction()
        if confirm:
            return redirect(url_for('initial',room_id=room_id))

    dic=CURRENT_ROOM.set_data_choose_devices(use_related=True)
    img=CURRENT_ROOM.image_360
    #print(dic)
    return render_template('device.html',dic=dic,img=img)

@app.route("/search", methods=['POST','GET'])
def search():
    room_id=''
    if request.method == "POST":
        room_id=request.form.get('room_id')
        return redirect(url_for('room',room_id=room_id))

    return render_template('search.html',room_id=room_id,roomInfo_book=roomInfo_book,roomInfo_recent=roomInfo_recent,roomInfo_result=roomInfo_result)

@app.route("/room/<room_id>", methods=['POST','GET'])
def room(room_id):
    if request.method == "POST":
        CURRENT_ROOM(room_id=room_id)
        if request.form.get('enter'):
            return redirect(url_for('device',room_id=CURRENT_ROOM.room_id))
        elif request.form.get('book'):
            return redirect(url_for('booking',room_name='5554'))
    
    return render_template('room.html')

@app.route("/booking/<room_name>", methods=['POST','GET'])
def booking(room_name):
    if request.method == "POST":
        if request.form.get('back'):
            return redirect(url_for('room',room_id=room_name))
        elif request.form.get('home'):
            return render_template('search.html',room_id=room_name)
        elif request.form.get('book'):
            CURRENT_ROOM.get_booking_result()
            return  redirect(url_for('room',room_id=room_name))

    time=CURRENT_ROOM.booking_time
    week=CURRENT_ROOM.set_booking_week()
    month=MONTH_ABBR[CURRENT_ROOM.today_date[1]]
    year=CURRENT_ROOM.today_date[0]
    occupy=CURRENT_ROOM.set_booking_occupy()
    return render_template('booking.html',room=room_name,time=time,week=week,month=month,year=year,occupy=occupy)

@app.route("/personal-device", methods=['POST','GET'])
def personal_device():
    if request.method == "POST":
        device=[]
        for d in PERSONAL_TYPE:
            if request.form.get(d):
                device.append(d)

        #global CURRENT_ROOM
        CURRENT_ROOM.get_data_personal_device(device)
        CURRENT_ROOM.set_data_instruction()

        return redirect(url_for('device',room_id=CURRENT_ROOM.room_id))

    return render_template('personal-device.html')

@app.route("/instruction-choose", methods=['POST','GET'])
def instructor_choose():
    #global CURRENT_ROOM
    if request.method == "POST":
        device=request.form.get('input')
        CURRENT_ROOM.create_guide_queue(device)
        return redirect(url_for('instruction'))
    
    img=CURRENT_ROOM.image_360
    dic=CURRENT_ROOM.choose_devices_relative(use_related=False)
    order=CURRENT_ROOM.get_guide_order()
    #pprint(dic)
    #pprint(CURRENT_ROOM.image_360_deivces)
    #pprint(CURRENT_ROOM.image_360_deivces_related)
    return render_template('instruction-choose.html',dic=dic, image_path=img, order=order)

@app.route("/instruction", methods=['POST','GET'])
def instruction():
    #global CURRENT_ROOM
    guide=None
    if request.method == "POST":
        if len(CURRENT_ROOM.guide_queque)==0:
            return redirect(url_for('instructor_choose'))
        else:
            guide=CURRENT_ROOM.pop_guide_queue()
            return render_template('instruction.html',title="Guide of "+CURRENT_ROOM.guide_device,guide=guide)

    guide=CURRENT_ROOM.pop_guide_queue()
    return render_template('instruction.html',title="Guide of "+CURRENT_ROOM.guide_device,guide=guide)

steps={
   'step 1':{'text':'Find the HDMI cable underneath the conference table', 'image':'', 'command':"print('instruction_initial_list')\r\nprint(steps)", 'help':''},
   'step 2':{'text':'Find the HDMI cable underneath the conference table', 'image':'8bdd60db4a154e428fd47f7d857b8cf9', 'command':"print('instruction_initial_list')\r\nprint(steps)", 'help':'helpxxxxxxxx xxxxxxxxxxxxxxx xxxxxxxxxxxx xxxxxxxxxxxx xxxxxxxxxxx'},
   'step 3':{'text':'Plug the HDMI cable to your laptop', 'image':'8bdd60db4a154e428fd47f7d857b8cf9', 'command':'', 'help':''},
}

@app.route("/initial", methods=['POST','GET'])
def initial():
    print("initial")
    print(steps)
    room_id = request.args.get('room_id')
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('turnon',room_id=CURRENT_ROOM.room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('device',room_id=CURRENT_ROOM.room_id))
    
    return render_template('instruction_initial.html',room_id=CURRENT_ROOM.room_id,steps=steps)

@app.route("/turnon", methods=['POST','GET'])
def turnon():
    print("turnon")
    print(steps)
    room_id = request.args.get('room_id')
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('pair',room_id=CURRENT_ROOM.room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('initial',room_id=CURRENT_ROOM.room_id))
    
    return render_template('instruction_turnon.html',room_id=CURRENT_ROOM.room_id,steps=steps)

@app.route("/pair", methods=['POST','GET'])
def pair():
    print("pair")
    print(steps)
    room_id = request.args.get('room_id')
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('zoom',room_id=CURRENT_ROOM.room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('turnon',room_id=CURRENT_ROOM.room_id))
    
    return render_template('instruction_pair.html',room_id=CURRENT_ROOM.room_id,steps=steps)

@app.route("/zoom", methods=['POST','GET'])
def zoom():
    print("zoom")
    print(steps)
    room_id = request.args.get('room_id')
    if request.method == "POST":
        next=request.form.get('next')
        if next:
            return redirect(url_for('search'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('pair',room_id=CURRENT_ROOM.room_id))
    
    return render_template('instruction_zoom.html',room_id=CURRENT_ROOM.room_id,steps=steps)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)