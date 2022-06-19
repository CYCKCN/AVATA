import os
from app import db
from app.img_trans import *

def path_exist_or_mkdir(path:str):
    #找地址 找不到就创建
    if not os.path.exists(path):
        os.makedirs(path)
    return True

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
    #name image loc可以全改或改几个 但是不能全都不改 不然false
    #room_id当前房间的名字要是不存在 返回false
    #name更改后房间的名字存在会冲突 返回false
    if not room_is_exist(room_id): return False
    if room_is_exist(name): return False
    if name==None and image==None and loc==None: return False
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
    room=find_room_with_name(name)
    if room==None: return False
    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)
    path=f'app/static/images/test/room{name}/_basic_upload.png'
    image_decoder(room['roomImage'],path)
    return True

