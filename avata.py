import os
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Flask
from easydict import EasyDict

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

        return device

    return render_template('device.html',dic=demo_dic())

@app.route("/search", methods=['POST','GET'])
def search():
    room_id=''
    if request.method == "POST":
        room_id=request.form.get('room_id')
        return room_id

    return render_template('search.html',room_id=room_id)

@app.route("/instruction-choose", methods=['POST','GET'])
def instructor_choose():
    if request.method == "POST":
        name=request.form.get('input')
        return name
    
    image_path=url_for('static',filename='images/grey.jpg')
    return render_template('instruction-choose.html',dic=demo_dic(300,300), image_path=image_path)

@app.route("/instruction", methods=['POST','GET'])
def instruction():
    if request.method == "POST":
        return "submit"

    title="guide title"
    guide={}
    img=['grey.jpg','grey.jpg','grey.jpg']
    text=['text1','text2','text3']
    step_num=len(img)
    for i in range(step_num):
        guide[text[i]]=url_for('static',filename='images/'+img[i])
    return render_template('instruction.html',title=title,guide=guide)


if __name__ == "__main__":
    app.run(debug=True)