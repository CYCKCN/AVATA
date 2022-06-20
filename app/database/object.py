class Account(object):
    def __init__(self, email, password, identity="USER"):
        self.accountEmail = email # "example@example.com"
        self.accountPw = password # "examplePW"
        self.accountID = identity # "USER" / "ADMIN"

class Device(object):
    def __init__(self, deviceID, roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY):
        self.deviceID = deviceID
        self.roomName = roomName # "IEDA Conference Room, Room 5554"
        self.deviceName = deviceName # "project_1"
        self.deviceType = deviceType # "display_projector_WIFI"
        self.deviceIP = deviceIP # "000.00.000.000:0000"
        self.deviceLocX = deviceLocX # 1
        self.deviceLocY = deviceLocY # 2

class Room(object):
    def __init__(self, roomName, roomImg, roomLoc):
        self.roomName = roomName # "IEDA Conference Room, Room 5554"
        self.roomImg = roomImg # ""
        self.roomLoc = roomLoc # "Academic Building"
        self.room360Img = ""
        self.bookBy = {}
        self.bookTime = {}
        self.insInitial = []
        self.insTurnon = {}
        self.insPair = []
        self.insZoom = {"video": [], "audio": []}