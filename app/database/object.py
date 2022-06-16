from pymongo.mongo_client import MongoClient
import datetime

class Account(object):
    def __init__(self, email, password, identity="USER"):
        self.email = email
        self.password = password
        self.identity = identity

    def change_identity(self, identity):
        self.identity = identity

class Room(object):
    def __init__(self, room_name, image):
        self.room_name = room_name # 4223 / ISD works
        self.location = image
        self.booking = {}
        self.available = {}
    

class Device(object):
    def __init__(self, name, t, loc=None, status=False):
        self.name = name
        self.type = t
        self.location = loc
        self.controllers = []
        self.predevices = []
        self.codevices = []
        self.subdevices = []
        self.status = status
    
    def build_controller(self, controller):
        if controller.name not in self.controllers:
            self.controllers.append(controller.name)
        return 
    
    def build_predevices(self, device):
        if device.name not in self.predevices:
            self.predevices.append(device.name)
        return 

    def build_codevices(self, device):
        if device.name not in self.codevices:
            self.codevices.append(device.name)
        return 

    def build_subdevices(self, device):
        if device.name not in self.subdevices:
            self.subdevices.append(device.name)
        return 

class Controller(object):
    def __init__(self, name, t, fon, fconnection, loc=None):
        self.name = name
        self.type = t
        self.location = loc
        self.functions = {"ON": fon, "CONNECTION": fconnection}
        self.todevices = {"ON": [], "CONNECTION": []}
        self.remarks = {"ON":[], "CONNECTION": []}

    def build_todevices(self, f, device, r):
        if self.functions[f] == True:
            if device.name not in self.todevices[f]:
                self.todevices[f].append(device.name)
                self.remarks[f].append(r)
