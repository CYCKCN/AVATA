class Account(object):
    def __init__(self, email, password, identity="USER"):
        self.accountEmail = email # "example@example.com"
        self.accountPw = password # "examplePW"
        self.accountID = identity # "USER" / "ADMIN"

class Device(object):
    def __init__(self, roomName, deviceName, deviceType, deviceIP, deviceLoc):
        self.roomName = roomName # ["IEDA Conference Room", "5554"]
        self.deviceName = deviceName # "project_1"
        self.deviceType = deviceType # "display_projector_WIFI"
        self.deviceIP = deviceIP # "000.00.000.000:0000"
        self.deviceLoc = deviceLoc # [0, 0]

class Room(object):
    def __init__(self, roomName, roomImg, roomLoc, bookBy, bookTime, insInitial, insTurnon, insPair, insZoom):
        self.roomName = roomName
        self.roomImg = roomImg
        self.roomLoc = roomLoc
        self.bookBy = bookBy
        self.bookTime = bookTime
        self.insInitial = insInitial
        self.insTurnon = insTurnon
        self.insPair = insPair
        self.insZoom = insZoom