import os
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Flask
from easydict import EasyDict

import demo_utils
from test_data import ROOM, PERSONAL_TYPE

PATH_templates='frontend/templates'
PATH_static='frontend/static'

app = Flask(__name__, template_folder=PATH_templates, static_folder=PATH_static)
#app = Flask(__name__)

CURRENT_ROOM=ROOM(oscwd=os.getcwd())

@app.route("/")
def hello():
    return 'hello'

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        if email:
            return redirect(url_for('verification', email=email))

    return render_template('login.html')

@app.route("/verification/<email>", methods=['POST','GET'])
def verification(email):
    if request.method == "POST":
        code = request.form.get('code')
        if code:
            return redirect(url_for('search'))

    return render_template('verification-code.html', userEmail=email)

'''
@app.route("/device", methods=['POST','GET'])
def demo():
    if request.method == "POST":
        confirm=request.form.get('confirm')
        device={}
        dic_=demo_dic()
        for i, d in dic_.items():
            if request.form.get(d['name']):
                device[i]=request.form.get(d['name'])
            else: device[i]=''

        #return device
        return redirect(url_for('instructor_choose'))

    return render_template('device.html',dic=demo_dic())
'''
@app.route("/device", methods=['POST','GET'])
def device():
    #global CURRENT_ROOM
    if request.method == "POST":
        CURRENT_ROOM.get_data_choose_devices()
        return redirect(url_for('personal_device'))

    dic=CURRENT_ROOM.set_data_choose_devices()
    img=CURRENT_ROOM.image_360
    #print(dic)
    return render_template('device.html',dic=dic,img=img)

@app.route("/search", methods=['POST','GET'])
def search():
    room_id=''
    if request.method == "POST":
        room_id=request.form.get('room_id')
        return redirect(url_for('room'))

    return render_template('search.html',room_id=room_id)

'''
@app.route("/room", methods=['POST','GET'])
def room():
    if request.method == "POST":

        return ""

    return render_template('room.html')

@app.route("/personal-device", methods=['POST','GET'])
def personal_device():
    if request.method == "POST":

        return ""

    return render_template('personal-device.html')
'''

@app.route("/room", methods=['POST','GET'])
def room():
    if request.method == "POST":
        request.form.get('input')
        #global CURRENT_ROOM
        CURRENT_ROOM(room_id='room1')
        return redirect(url_for('device'))

    return render_template('room.html')

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

        return redirect(url_for('instructor_choose'))

    return render_template('personal-device.html')


'''
Personal=[]
@app.route("/instruction-choose", methods=['POST','GET'])
def instructor_choose():
    if request.method == "POST":
        name=request.form.get('input')
        global Personal
        Personal=demo_utils.create_queue(os.getcwd(),'win')
        #print(Personal)
        return redirect(url_for('instruction', idx=name))
    
    image_path=url_for('static',filename='images/demo-ieda/short.png')
    return render_template('instruction-choose.html',dic=demo_dic1, image_path=image_path)

@app.route("/instruction/<idx>", methods=['POST','GET'])
def instruction(idx):
    if request.method == "POST":
        global Personal
        if len(Personal)==0:
            for _, elem in demo_dic1.items():
                if(elem['name']==idx):
                    elem['clicked']='y'
            return redirect(url_for('instructor_choose'))
        else: 
            guide=Personal.pop(0)
            return render_template('instruction.html',title="Guide",guide=guide)

    guide=Personal.pop(0)

    return render_template('instruction.html',title="Guide",guide=guide)

'''

@app.route("/instruction-choose", methods=['POST','GET'])
def instructor_choose():
    #global CURRENT_ROOM
    if request.method == "POST":
        device=request.form.get('input')
        CURRENT_ROOM.create_guide_queue(device)
        return redirect(url_for('instruction'))
    
    img=CURRENT_ROOM.image_360
    dic=CURRENT_ROOM.choose_devices_relative()
    order=CURRENT_ROOM.get_guide_order()
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


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)