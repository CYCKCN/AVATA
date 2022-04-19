class Account(object):
    def __init__(self, email, rmid):
        self.email = email
        self.rmid = rmid
        self.check_identity()

    def check_identity(self):
        if "ust.hk" in self.email:
            self.identity = "USER"
            self.request = False
        else:
            self.identity = "GUEST"
            self.request = True


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
