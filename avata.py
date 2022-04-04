import os
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Flask
from easydict import EasyDict

import demo_utils

PATH_templates='frontend/templates'
PATH_static='frontend/static'

app = Flask(__name__, template_folder=PATH_templates, static_folder=PATH_static)
#app = Flask(__name__)

@app.route("/")
def hello():
    return 'hello'

def demo_dic(H=1080,W=1920):
    dic={#1080*1920
        0:{
            'name':'d1',
            'v':str(int(H*0.2))+'px',
            'u':str(int(W*0.2))+'px'
        },
        1:{
            'name':'d2',
            'v':str(int(H*0.8))+'px',
            'u':str(int(W*0.3))+'px'
        },
        2:{
            'name':'d3',
            'v':str(int(H*0.1))+'px',
            'u':str(int(W*0.6))+'px'
        }
    }
    return dic

# def demo_dic1(H=500,W=450):
    '''
    dic={#1080*1920
        0:{
            'name':'d1',
            'v':str(int(H*0.2))+'px',
            'u':str(int(W*0.75))+'px'
        },
        1:{
            'name':'d2',
            'v':str(int(H*0.7))+'px',
            'u':str(int(W*0.2))+'px'
        }
    }
    '''
demo_dic1={#1080*1920
    0:{
        'name':'1',
        'v':'20%',
        'u':'75%',
        'clicked':'n'  # y:clicked; n:not clicked (original state)
    },
    1:{
        'name':'2',
        'v':'70%',
        'u':'20%',
        'clicked':'n'
    }
}

#    return dic

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

@app.route("/search", methods=['POST','GET'])
def search():
    room_id=''
    if request.method == "POST":
        room_id=request.form.get('room_id')
        return redirect(url_for('room'))

    return render_template('search.html',room_id=room_id)

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

    '''
    title="guide title"
    guide={}
    img=['grey.jpg','grey.jpg','grey.jpg']
    text=['text1','text2','text3']
    step_num=len(img)
    for i in range(step_num):
        guide[text[i]]=url_for('static',filename='images/'+img[i])
    '''

    guide=Personal.pop(0)

    return render_template('instruction.html',title="Guide",guide=guide)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)