from pymongo import MongoClient

def connection(dbname):
    # mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true"&"w=majority
    addr = "mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(addr)
    db = client[dbname]
    return db

from .models import Account, Device, Room

class AccountDB():
    def __init__(self, db):
        self.db = db["account"]

    def signup(self, accountEmail, accountPw):
        if self.db.find_one({"accountEmail": accountEmail}):
            return "Err: Account Exists!"
        newAccount = Account(accountEmail, accountPw)
        self.db.insert_one(newAccount.__dict__)
        return "Info: Register USER Account Successfully"

    def login(self, accountEmail, accountPw, loginID):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered! Try Login as GUEST!"
        elif account["accountPw"] != accountPw:
            return "Err: Wrong Password!"
        elif account["accountID"] != loginID:
            return "Err: You Are Not Authorized!"
        else:
            return "Info: Login successfully!"
    
    def checkAccountID(self, accountEmail):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        return account["accountID"]

    def updateAdminID(self, accountEmail):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        self.db.update_one({"accountEmail": accountEmail}, {'$set': {'accountID': "ADMIN"}})
        return 

class DeviceDB():
    def __init__(self, db):
        self.db = db["device"]

    def addDevice(self, roomName, deviceName, deviceType, deviceIP, deviceLoc):
        device = self.db.find_one({"deviceLoc": deviceLoc})
        if device:
            self.delDevice(roomName, deviceLoc)
        newDevice = Device(roomName, deviceName, deviceType, deviceIP, deviceLoc)
        self.db.insert_one(newDevice.__dict__)
        return "Info: Add Device Successfully"
            
    def delDevice(self, roomName, deviceLoc):
        device = self.db.find_one({"deviceLoc": deviceLoc})
        if device is None:
            return "Err: Device Invalid"
        self.db.remove({"_id": device["_id"]})
        return "Info: Delete Successfully"
    
    def checkDeviceList(self, roomName):
        devices = self.db.find({"roomName": roomName})
        return devices
    
    def printDeviceList(self, roomName):
        devices = self.checkDeviceList(roomName)
        for dev in devices:
            print("Device Name: " + dev["deviceName"] + "\nDevice Type: " + dev["deviceName"] + "\nDevice IP" + dev["deviceIP"])


class RoomDB():
    def __init__(self, db):
        self.db = db["room"]