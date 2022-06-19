import os
from app import db
from app.img_trans import *

def path_exist_or_mkdir(path:str):
    #找地址 找不到就创建
    if not os.path.exists(path):
        os.makedirs(path)
    return True

#------------ Room utils ---------------

def find_room_with_name(name:str):
    #用name找room 找不到返回false
    _db=db['rooms']
    room=_db.find_one({'roomName':name})
    if room: return room
    else: return False

def room_is_exist(name:str):
    #检查room存不存在 存在true不存在false name不合法false
    if name==None:  return False
    _db=db['rooms']
    if _db.find_one({'roomName':name}): return True
    else: return False

def room_has_attribute(name:str,attr:str):
    _db=db['rooms']
    room=_db.find({'roomName':name,attr:{'$exists': True}})
    if room: return True
    else: return False

def get_room_location_with_name(name:str):
    room=find_room_with_name(name)
    return room['roomLoc']

def create_room_with_name_image_loc(name:str, image:str, loc:str):
    #用name image loc创建新的room
    _db=db['rooms']
    _dict={
        'roomName':name,
        'roomImage':image,
        'roomLoc':loc
    }
    _db.insert_one(_dict)
    return True

def update_room_with_name_image_loc(room_id:str ,name:str=None, image:str=None, loc:str=None):
    #room_id是现在这个room的名字
    #name是更改后房间的名字 image loc同理
    #name image loc可以全改或改几个 全都不改返回True
    #room_id当前房间的名字要是不存在 返回false
    #name更改后房间的名字存在会冲突 返回false
    if not room_is_exist(room_id): return False
    if room_is_exist(name): return False
    if name==None and image==None and loc==None: return True
    _db=db['rooms']
    room=find_room_with_name(room_id)
    _dict={}
    if name: _dict['roomName']=name
    if image: _dict['roomImage']=image
    if loc: _dict['roomLoc']=loc
    _db.update_one(
        {'_id': room['_id']}, 
        {'$set': _dict}
    )
    return True

def download_room_basic_image_with_name(name:str):
    #缓存当前房间basic的图片
    room=find_room_with_name(name)
    if room==None: return False
    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)

    #if room['roomImage']==None: return False
    path=f'app/static/images/test/room{name}/_basic_upload.png'
    image_decoder(room['roomImage'],path)

    return True

def get_all_room_basic():
    #date和time还没有加 后面记得加
    _db=db['rooms']
    if _db.count_documents({})==0: return False

    rooms=_db.find({})
    _dict={}
    i=0
    for room in rooms:
        _d={}
        _d['name']=room['roomName']
        _d['lift']=room['roomLoc']
        #_d['date']=
        #_d['time']=

        _dict[i]=_d
        download_room_basic_image_with_name(_d['name'])
        i+=1
    
    return _dict

def delete_room_with_name(name:str):
    if name==None: return False
    if not room_is_exist(name): return False
    _db=db['rooms']
    _db.delete_one({'roomName':name})
    return True

def add_room_360image_with_name(name:str,image:str=None):
    if name==None: return False
    if image==None: return True
    if not room_is_exist(name): return False
    _db=db['rooms']
    _db.update_one(
        {'roomName':name},
        {'$set':{'room360Image':image}}
    )
    return True

def download_room_360image_with_name(name:str):
    if name==None: return False
    if not room_is_exist(name): return False
    room=find_room_with_name(name)
    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)

    if not room_has_attribute(name,'room360Image'): return False
    path=f'app/static/images/test/room{name}/_360_upload.png'
    image_decoder(room['room360Image'],path)

    return True


#------------ Device utils ---------------

def device_is_exist(room:str,id:int):
    _db=db['devices']
    device=_db.find_one({'roomName':room,'deviceId':id})
    if device: return True
    else: return False

def create_device_with_room_id_name_type_x_y(
    room:str,id:int,name:str,type:str,x:str,y:str):
    _db=db['devices']
    _dict={
        'roomName':room,
        'deviceId':id,
        'deviceName':name,
        'deviceType':type,
        'deviceX':x,
        'deviceY':y
    }
    _db.insert_one(_dict)
    return True


def get_all_devices_with_room(name:str):
    _db=db['devices']
    if _db.count_documents({'roomName':name})==0: return False
    devices=_db.find({'roomName':name})
    _dict={}
    for device in devices:
        _d={
            'name':device['deviceName'],
            'type':device['deviceType'],
            'x':device['deviceX'],
            'y':device['deviceY']
        }
        _dict[device['id']]=_d
    return _dict

def update_device_with_name_type_x_y(room:str,id:int,name:str=None,type:str=None,x:str=None,y:str=None):
    _db=db['devices']
    if not device_is_exist(room,id): return False
    if name==None and name==None and type==None and x==None and y==None: return True
    _dict={}
    if name: _dict['deviceName']=name
    if type: _dict['deviceType']=type
    if x: _dict['deviceX']=x
    if y: _dict['deviceY']=y
    _db.update_one(
        {'roomName':room, 'deviceId':id},
        {'$set':_dict}
    )
    return True
