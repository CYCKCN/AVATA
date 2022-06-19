import os
from app import db

def path_exist_or_mkdir(path:str):
    if not os.path.exists(path):
        os.makedirs(path)
    return True

def find_room_with_name(name:str):
    _db=db['rooms']
    room=_db.find_one({'roomName':name})
    if room: return room
    else: return False

def room_is_exist(name:str):
    _db=db['rooms']
    if _db.find_one({'roomName':name}): return True
    else: return False

def create_room_with_name_image_loc(name:str, image:str, loc:str):
    _db=db['rooms']
    _dict={
        'roomName':name,
        'roomImage':image,
        'roomLoc':loc
    }
    _db.insert_one(_dict)
    return True

def update_room_with_name_image_loc(room_id:str ,name:str=None, image:str=None, loc:str=None):
    if not room_is_exist(room_id): return False
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


