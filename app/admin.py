import os
from flask import Blueprint, render_template, redirect, url_for, request
from .authen import check_login
from .img_trans import *
from app import accountdb, devicedb, roomdb
import utils
from flask_login import logout_user

admin_blue=Blueprint('admin',__name__,url_prefix='/admin')

@admin_blue.route('/')
def enter():
    return 'admin flow'

@admin_blue.route("/logout", methods=['GET'])
def logout():  
    logout_user()
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
    '''
    roomInfo={
        0:{'name':'5554','lift':'27-28','date':'August 21','time':'19:00-21:00'},
        1:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        2:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        3:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        4:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        5:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        6:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
    }'''
    error=request.args.get('error')
    if request.method == "POST":
        room_id=request.form.get('room_id') if not request.form.get('room_id')=='' else request.form.get('roomid')
        add=request.form.get('add')

        if add:
            return redirect(url_for('admin.basic_info',is_addRoom=True))

        btn_profile=request.form.get('profile')
        if btn_profile:
            return redirect(url_for('admin.profile'))
        
        if not utils.room_is_exist(room_id):
            return redirect(url_for('admin.main',error='Room not exists!'))

        if room_id:
            return redirect(url_for('admin.room',room_id=room_id))
        
    roomInfo=utils.get_all_room_basic()
    return render_template('admin_main.html',
    roomInfo=roomInfo,
    error=error if error else '')

@admin_blue.route("/room/<room_id>", methods=['POST','GET'])
@check_login 
def room(room_id):
    error=request.args.get('error')
    
    if request.method == "POST":
        edit=request.form.get('edit')
        if edit:
            return redirect(url_for('admin.basic_info',room_id=room_id,is_editRoom=True))
        delete=request.form.get('delete')
        if delete:
            utils.delete_room_with_name(room_id)
            return redirect(url_for('admin.main'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.main'))
    
    utils.download_room_basic_image_with_name(room_id)
    return render_template('admin_room.html',
    room_id=room_id,
    room_loc=utils.get_room_location_with_name(room_id),
    error=error if error else '')

@admin_blue.route("/basic_info", methods=['POST','GET'])
@check_login 
def basic_info():
    room_id = request.args.get('room_id')
    is_addRoom = request.args.get('is_addRoom')
    is_editRoom = request.args.get('is_editRoom')

    if is_editRoom:
        utils.download_room_basic_image_with_name(room_id)

    if request.method == "POST":
        continue_=request.form.get('continue')
        if is_addRoom and continue_:
            #roomName
            roomName=request.form.get('room_id')
            if utils.room_is_exist(roomName):
                return redirect(url_for('admin.room',room_id=roomName,is_editRoom=True,error='Room exists, please edit the room.'))

            #roomImage
            img_base64=request.form.get('imgSrc')
            roomImage=(img_base64.split(','))[-1]
            if len(roomImage)==0:
                return redirect(url_for('admin.basic_info',is_addRoom=True))

            #roomLoc
            roomLoc=request.form.get('room_loc')

            utils.create_room_with_name_image_loc(roomName, roomImage, roomLoc)
            return redirect(url_for('admin.photo_360',room_id=room_id,is_addRoom=True))
        
        if is_editRoom and continue_:
            roomName = request.form.get('room_id') if request.form.get('room_id') else None
            roomLoc = request.form.get('room_loc') if request.form.get('room_loc') else None
            
            img_base64=request.form.get('imgSrc')
            roomImage=(img_base64.split(','))[-1] if img_base64 else None
            has_udpate=utils.update_room_with_name_image_loc(room_id, roomName, roomImage, roomLoc)

            if has_udpate:
                return redirect(url_for('admin.photo_360',
                room_id=roomName if roomName else room_id,
                is_editRoom=True))
            else:
                return redirect(url_for('admin.room',room_id=roomName,is_editRoom=True,error='Invalid room name or empty submit!'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.room',room_id=room_id))
            

        #if continue_:
        #    return redirect(url_for('admin.photo_360',room_id=room_id))
    
    return render_template('admin_basic_info.html',
    room_id=room_id if is_editRoom else '1234',
    is_addRoom=True if is_addRoom else False,
    is_editRoom=True if is_editRoom else False)

@admin_blue.route("/photo_360", methods=['POST','GET'])
def photo_360():
    room_id = request.args.get('room_id')
    is_addRoom = request.args.get('is_addRoom')
    is_editRoom = request.args.get('is_editRoom')
    if request.method == "POST":
        continue_=request.form.get('continue')
        img360_base64=request.form.get('img360Src')
        room360Image=(img360_base64.split(','))[-1] if img360_base64 else None
        #if len(room360Image)==0:
        #    return redirect(url_for('admin.photo_360',is_addRoom=True))
        utils.add_room_360image_with_name(room_id,room360Image)

        if is_addRoom and continue_:
            return redirect(url_for('admin.device_info',room_id=room_id,is_addRoom=True))

        if is_editRoom and continue_:
            return redirect(url_for('admin.device_info',room_id=room_id,is_editRoom=True))

        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.basic_info',room_id=room_id))


        '''
        img360_base64=request.form.get('img360Src')
        image_decoder((img360_base64.split(','))[-1],
        f'app/static/images/test/room{room_id}/_360_upload.png')
        #rint(img360_base64)
        if continue_:
            return redirect(url_for('admin.device_info',room_id=room_id))
        '''

    utils.download_room_360image_with_name(room_id)
    return render_template('admin_360_photo.html',
    room_id=room_id,
    is_addRoom=True if is_addRoom else False,
    is_editRoom=True if is_editRoom else False)


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
            return redirect(url_for('admin.instruction_initial_list',room_id=room_id))
        if checklist:
            return redirect(url_for('admin.device_list',room_id=room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.photo_360',room_id=room_id))

        update_from_admin_request(devices_dict[room_id])
    
    devices=utils.get_all_devices_with_room(room_id)
    devices_choose=utils.get_choose_device_with_room(room_id)
    #return render_template('admin_device_info.html',room_id=room_id,devices=devices_dict[room_id].getJson(),devices_choose=devices_dict[room_id].chooseDevice())
    return render_template('admin_device_info.html',room_id=room_id,devices=devices,devices_choose=devices_choose)

@admin_blue.route("/device_list", methods=['GET'])
def device_list():
    room_id = request.args.get('room_id')
    if request.method == "POST":
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.device_info',room_id=room_id))

    return render_template('admin_device_list.html',room_id=room_id,devices=devices_dict[room_id].getJson())

steps={
    'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
}

@admin_blue.route("/instruction_initial_list", methods=['POST','GET'])
def instruction_initial_list():
    room_id = request.args.get('room_id')
    print("instruction_initial_list")
    print(steps)
    print(devices_dict)

    if request.method == "POST":
        # add
        if request.form.get(f'add-step'):
            print("add")
            step_length = f"step {len(steps.keys())+1}"
            new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
            steps.update(new_dict)
            print(steps)
            return redirect(url_for('admin.instruction_initial',room_id=room_id,step_id=step_length))
        
        for step_id in steps.keys():
            # edit
            if request.form.get(f'edit_{step_id}'):
                print("edit", step_id)
                return redirect(url_for('admin.instruction_initial',room_id=room_id,step_id=step_id))
            # delete
            if request.form.get(f'delete_{step_id}'):
                print("delete", step_id)
                return render_template('admin_instruction_initial_list.html',room_id=room_id,steps=steps)
        confirm=request.form.get('confirm')
        if  confirm:
            return redirect(url_for('admin.instruction_turnon_main',room_id=room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.device_info',room_id=room_id))
    
    return render_template('admin_instruction_initial_list.html',room_id=room_id,steps=steps)

@admin_blue.route("/instruction_initial", methods=['POST','GET'])
def instruction_initial():
    print("instruction_initial")
    print(devices_dict)
    print(steps)
    room_id = request.args.get('room_id')
    step_id = request.args.get('step_id')
    if request.method == "POST":
        step_text=request.form.get('step_text')
        img_base64=request.form.get('imgSrc')
        step_command=request.form.get('step_command')
        step_help=request.form.get('step_help')
        print(step_text)
        print(img_base64)
        print(step_command)
        print(step_help)
        confirm=request.form.get('confirm')
        if confirm:
            steps[step_id]["text"]=step_text
            steps[step_id]["image"]=img_base64  # debug
            steps[step_id]["command"]=step_command
            steps[step_id]["help"]=step_help
            print(steps)
            return redirect(url_for('admin.instruction_initial_list',room_id=room_id))
    
    return render_template('admin_instruction_initial.html',room_id=room_id,step_id=step_id,steps=steps)

@admin_blue.route("/instruction_turnon_main", methods=['POST','GET'])
def instruction_turnon_main(): 
    room_id = request.args.get('room_id')
    print(devices_dict)
    if request.method == "POST":
        for device_id in range(0, len(devices_dict[room_id].devices)):
            # edit
            if request.form.get(f'edit_{device_id}'):
                print("edit", device_id)
                device_id+=1
                return redirect(url_for('admin.instruction_turnon_list',room_id=room_id,device_id=device_id))
        confirm=request.form.get('confirm')
        if confirm:
            return redirect(url_for('admin.instruction_pair_main',devices_obj=devices_dict[room_id],room_id=room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.instruction_initial_list',room_id=room_id))
    return render_template('admin_instruction_turnon_main.html',devices_obj=devices_dict[room_id],room_id=room_id)

@admin_blue.route("/instruction_turnon_list", methods=['POST','GET'])
def instruction_turnon_list():  
    room_id = request.args.get('room_id')
    device_id = request.args.get('device_id')
    print("instruction_turnon_list")
    print(steps)

    if request.method == "POST":
        # add
        if request.form.get(f'add-step'):
            print("add")
            step_length = f"step {len(steps.keys())+1}"
            new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
            steps.update(new_dict)
            print(steps)
            return redirect(url_for('admin.instruction_turnon',device_id=device_id,room_id=room_id,step_id=step_length))
        
        for step_id in steps.keys():
            # edit
            if request.form.get(f'edit_{step_id}'):
                print("edit", step_id)
                # not implemented delete function
                return redirect(url_for('admin.instruction_turnon',device_id=device_id,room_id=room_id,step_id=step_id))
            # delete
            if request.form.get(f'delete_{step_id}'):
                print("delete", step_id)
                return render_template('admin_instruction_turnon_list.html',device_id=device_id,room_id=room_id,steps=steps)
        confirm=request.form.get('confirm')
        if confirm:
            return redirect(url_for('admin.instruction_turnon_main',devices_obj=devices_dict[room_id],room_id=room_id))
    return render_template('admin_instruction_turnon_list.html',device_id=device_id,room_id=room_id,steps=steps)

@admin_blue.route("/instruction_turnon", methods=['POST','GET'])
def instruction_turnon():
    print("instruction_turnon")
    print(steps)
    room_id = request.args.get('room_id')
    step_id = request.args.get('step_id')
    device_id = request.args.get('device_id')
    if request.method == "POST":
        step_text=request.form.get('step_text')
        img_base64=request.form.get('imgSrc')
        step_command=request.form.get('step_command')
        step_help=request.form.get('step_help')
        print(step_text)
        print(img_base64)
        print(step_command)
        print(step_help)
        confirm=request.form.get('confirm')
        if confirm:
            steps[step_id]["text"]=step_text
            steps[step_id]["image"]=img_base64  # debug
            steps[step_id]["command"]=step_command
            steps[step_id]["help"]=step_help
            print(steps)
            return redirect(url_for('admin.instruction_turnon_list',device_id=device_id,room_id=room_id))
    
    return render_template('admin_instruction_turnon.html',device_id=device_id,room_id=room_id,step_id=step_id,steps=steps)

@admin_blue.route("/instruction_zoom_main", methods=['POST','GET'])
def instruction_zoom_main(): 
    room_id = request.args.get('room_id')
    video=request.form.get('edit_VIDEO')
    if request.method == "POST":
        if video:
            return redirect(url_for('admin.instruction_zoom_list',zoom_type='Video', room_id=room_id))
        audio=request.form.get('edit_AUDIO')
        if audio:
            return redirect(url_for('admin.instruction_zoom_list',zoom_type='Audio', room_id=room_id))
        confirm=request.form.get('confirm')
        if  confirm:
            return redirect(url_for('admin.room',room_id=room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.instruction_pair_main',devices_obj=devices_dict[room_id],room_id=room_id))
    
    return render_template('admin_instruction_zoom_main.html',room_id=room_id)

@admin_blue.route("/instruction_zoom_list", methods=['POST','GET'])
def instruction_zoom_list():  
    room_id = request.args.get('room_id')
    zoom_type = request.args.get('zoom_type')
    print("instruction_zoom_list")
    print(steps)

    if request.method == "POST":
        # add
        if request.form.get(f'add-step'):
            print("add")
            step_length = f"step {len(steps.keys())+1}"
            new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
            steps.update(new_dict)
            print(steps)
            return redirect(url_for('admin.instruction_zoom',room_id=room_id,step_id=step_length,zoom_type=zoom_type))
        
        for step_id in steps.keys():
            # edit
            if request.form.get(f'edit_{step_id}'):
                print("edit", step_id)
                # not implemented delete function
                return redirect(url_for('admin.instruction_zoom',room_id=room_id,step_id=step_id,zoom_type=zoom_type))
            # delete
            if request.form.get(f'delete_{step_id}'):
                print("delete", step_id)
                return render_template('admin_instruction_zoom_list.html',room_id=room_id,steps=steps,zoom_type=zoom_type)
        confirm=request.form.get('confirm')
        if  confirm:
            return redirect(url_for('admin.instruction_zoom_main',room_id=room_id,steps=steps, zoom_type=zoom_type))
    return render_template('admin_instruction_zoom_list.html',room_id=room_id,steps=steps, zoom_type=zoom_type)

@admin_blue.route("/instruction_zoom", methods=['POST','GET'])
def instruction_zoom():
    print("instruction_zoom")
    print(steps)
    room_id = request.args.get('room_id')
    step_id = request.args.get('step_id')
    zoom_type = request.args.get('zoom_type')
    if request.method == "POST":
        step_text=request.form.get('step_text')
        img_base64=request.form.get('imgSrc')
        step_command=request.form.get('step_command')
        step_help=request.form.get('step_help')
        print(step_text)
        print(img_base64)
        print(step_command)
        print(step_help)
        confirm=request.form.get('confirm')
        if confirm:
            steps[step_id]["text"]=step_text
            steps[step_id]["image"]=img_base64  # debug
            steps[step_id]["command"]=step_command
            steps[step_id]["help"]=step_help
            print(steps)
            return redirect(url_for('admin.instruction_zoom_list',room_id=room_id,zoom_type=zoom_type))
    
    return render_template('admin_instruction_zoom.html',room_id=room_id,step_id=step_id,steps=steps,zoom_type=zoom_type)

cases={
    'Case 1':{
        'devices':{
            'device 1':{'name':'device 1'},
            'device 3':{'name':'device 3'},
            'device 5':{'name':'device 5'},
        },
        'steps':{
            'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
        }
    },
    'Case 2':{
        'devices':{
            'device 2':{'name':'device 2'},
            'device 4':{'name':'device 4'},
        },
        'steps':{
            'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
        }
    },
    'Case 3':{
        'devices':{
            'device 1':{'name':'device 1'},
            'device 2':{'name':'device 2'},
            'device 4':{'name':'device 4'},
        },
        'steps':{
            'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
        }
    }
}
device111={
    'Device 1':{'name':'device 1'},
    'Device 2':{'name':'device 2'},
    'Device 3':{'name':'device 3'},
    'Device 4':{'name':'device 4'},
    'Device 5':{'name':'device 5'},
    'Apple':{'name':'Apple'},
    'Windows':{'name':'Windows'},
}

@admin_blue.route("/instruction_pair_main", methods=['POST','GET'])
def instruction_pair_main():
    room_id = request.args.get('room_id')
    print("instruction_pair_main")

    if request.method == "POST":
        # add
        if request.form.get(f'add-step'):
            print("add")
            case_length = f"case {len(cases.keys())+1}"
            new_dict = {case_length:{'devices':'', 'steps':''}}
            cases.update(new_dict)
            print(cases)
            return redirect(url_for('admin.instruction_pair_list',room_id=room_id,case_id=case_length))
        
        for case_id in cases.keys():
            # edit
            if request.form.get(f'edit_{case_id}'):
                print("edit", case_id)
                return redirect(url_for('admin.instruction_pair_list',room_id=room_id,case_id=case_id))
            # delete
            if request.form.get(f'delete_{case_id}'):
                print("delete", case_id)
                return render_template('admin_instruction_pair_main.html',room_id=room_id,cases=cases)
        confirm=request.form.get('confirm')
        if  confirm:
            return redirect(url_for('admin.instruction_zoom_main',room_id=room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.instruction_turnon_main',room_id=room_id))
    
    return render_template('admin_instruction_pair_main.html',room_id=room_id,cases=cases)

@admin_blue.route("/instruction_pair_list", methods=['POST','GET'])
def instruction_pair_list():  
    room_id = request.args.get('room_id')
    case_id = request.args.get('case_id')
    print("instruction_turnon_list")
    print(steps)

    if request.method == "POST":
        # add
        if request.form.get(f'add-step'):
            print("add")
            step_length = f"step {len(steps.keys())+1}"
            new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
            steps.update(new_dict)
            print(steps)
            return redirect(url_for('admin.instruction_pair',case_id=case_id,room_id=room_id,step_id=step_length))
        
        for step_id in steps.keys():
            # edit
            if request.form.get(f'edit_{step_id}'):
                print("edit", step_id)
                # not implemented delete function
                return redirect(url_for('admin.instruction_pair',case_id=case_id,room_id=room_id,step_id=step_id))
            # delete
            if request.form.get(f'delete_{step_id}'):
                print("delete", step_id)
                return render_template('admin_instruction_pair_list.html',case_id=case_id,room_id=room_id,steps=steps,device111=device111)
        confirm=request.form.get('confirm')
        if confirm:
            return redirect(url_for('admin.instruction_pair_main',room_id=room_id))
    return render_template('admin_instruction_pair_list.html',case_id=case_id,room_id=room_id,steps=steps,device111=device111)

@admin_blue.route("/instruction_pair", methods=['POST','GET'])
def instruction_pair():
    print("instruction_pair")
    print(steps)
    room_id = request.args.get('room_id')
    step_id = request.args.get('step_id')
    case_id = request.args.get('case_id')
    if request.method == "POST":
        step_text=request.form.get('step_text')
        img_base64=request.form.get('imgSrc')
        step_command=request.form.get('step_command')
        step_help=request.form.get('step_help')
        print(step_text)
        print(img_base64)
        print(step_command)
        print(step_help)
        confirm=request.form.get('confirm')
        if confirm:
            steps[step_id]["text"]=step_text
            steps[step_id]["image"]=img_base64  # debug
            steps[step_id]["command"]=step_command
            steps[step_id]["help"]=step_help
            print(steps)
            return redirect(url_for('admin.instruction_pair_list',case_id=case_id,room_id=room_id))
    
    return render_template('admin_instruction_pair.html',case_id=case_id,room_id=room_id,step_id=step_id,steps=steps)

@admin_blue.route("/profile", methods=['POST','GET'])
def profile():
    if request.method == "POST":
        btn_profile=request.form.get('profile')
        if btn_profile:
            return redirect(url_for('admin.main'))
        logout=request.form.get('logout')
        if logout:
            return redirect(url_for('admin.logout'))
    
    return render_template('admin_profile.html')
