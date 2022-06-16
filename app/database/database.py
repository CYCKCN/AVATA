import argparse
from unicodedata import name
import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from object import Account, Device, Controller
import argparse

# def get_parser():
#     parser = argparse.ArgumentParser(description="database development test")
#     parser.add_argument("--url", type=str, required=True, help="mongodb atlas connect your application")
#     parser.add_argument("--dbname", type=str, required=True, choices=['AVATA', 'AVATA_room', 'AVATA_account'])
#     return parser.parse_args()

def connection(dbname):
    # mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true"&"w=majority
    addr = "mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(addr)
    db = client[dbname]
    return db

if __name__ == '__main__':
    # args = get_parser()
    db = connection("AVATA")
    
    devices = db["devices"]
    controllers = db["controllers"]
    fs = GridFS(db)
    file = "ieda.jpg"
    with open(file, 'rb') as f:
        image = f.read()
    stored = fs.put(image, filename='files')

    projector1 = Device("projector1", "projector", stored)
    projector2 = Device("projector2", "projector")
    screen1 = Device("screen1", "screen")
    screen2 = Device("screen2", "screen")
    # mic1 = Device("mic1", "mic")
    # mic2 = Device("mic2", "mic")
    # boxspeaker1 = Device("boxspeaker1", "speaker")
    # boxspeaker2 = Device("boxspeaker2", "speaker")
    personalmac = Device("personalmac", "apple")

    projector1.build_codevices(screen1)
    projector1.build_subdevices(projector2)

    projector2.build_codevices(screen2)
    projector2.build_subdevices(projector1)

    screen1.build_codevices(projector1)
    screen1.build_subdevices(screen2)

    screen2.build_codevices(projector2)
    screen2.build_subdevices(screen1)

    personalmac.build_codevices(projector1)
    personalmac.build_codevices(projector2)
    personalmac.build_codevices(screen1)
    personalmac.build_codevices(screen2)

    extronpanel = Controller("extronpanel", "extron", True, False, stored)
    projector1RC = Controller("projector1 remote controller", "rc", True, False)
    projector2RC = Controller("projector2 remote controller", "rc", True, False)
    screen1switch = Controller("screen1 switch", "switch", True, False)
    screen2switch = Controller("screen2 switch", "switch", True, False)
    wifimodule = Controller("wifi module", "wifi", False, True)

    projector1.build_controller(extronpanel)
    extronpanel.build_todevices("ON", projector1, "Use extronpanel next to the door to turn on projector")
    projector1.build_controller(projector1RC)
    projector1RC.build_todevices("ON", projector1, "Use projector remote controller - 1 to turn on projector")

    projector2.build_controller(extronpanel)
    extronpanel.build_todevices("ON", projector2, "Use extronpanel next to the door to turn on projector")
    projector2.build_controller(projector2RC)
    projector2RC.build_todevices("ON", projector2, "Use projector remote controller - 2 to turn on projector")

    screen1.build_controller(extronpanel)
    extronpanel.build_todevices("ON", screen1, "Use extronpanel next to the door to turn on screen")
    screen1.build_controller(screen1switch)
    screen1switch.build_todevices("ON", screen1, "Use switch - 1 next to the door to turn on screen ")

    screen2.build_controller(extronpanel)
    extronpanel.build_todevices("ON", screen2, "Use extronpanel next to the door to turn on screen")
    screen2.build_controller(screen2switch)
    screen2switch.build_todevices("ON", screen2, "Use switch - 2 next to the door to turn on screen ")

    personalmac.build_controller(wifimodule)
    wifimodule.build_todevices("CONNECTION", personalmac, "Connect to wifi module shown on screen and use screen mirror for projection")

    devices.insert_one(projector1.__dict__)
    devices.insert_one(projector2.__dict__)
    devices.insert_one(screen1.__dict__)
    devices.insert_one(screen2.__dict__)
    devices.insert_one(personalmac.__dict__)

    controllers.insert_one(extronpanel.__dict__)    
    controllers.insert_one(projector1RC.__dict__)    
    controllers.insert_one(projector2RC.__dict__)    
    controllers.insert_one(screen1switch.__dict__)
    controllers.insert_one(screen2switch.__dict__)
    controllers.insert_one(wifimodule.__dict__)    