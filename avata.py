import os
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Flask

PATH_templates='frontend/templates'
PATH_static='frontend/static'

app = Flask(__name__, template_folder=PATH_templates, static_folder=PATH_static)
#app = Flask(__name__)

@app.route("/")
def hello():
    return 'hello'

H=1080
W=1920
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

@app.route("/demo", methods=['POST','GET'])
def demo():
    if request.method == "POST":
        confirm=request.form.get('confirm')
        device={}
        for i, d in dic.items():
            if request.form.get(d['name']):
                device[i]=request.form.get(d['name'])
            else: device[i]=''

        return device

    return render_template('demo.html',dic=dic)




if __name__ == "__main__":
    app.run(debug=True)