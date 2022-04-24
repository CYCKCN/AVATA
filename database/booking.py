import argparse
from unicodedata import name
import pymongo
from pymongo import MongoClient
import gridfs
from .object import Account, Device, Controller, Room
#from PIL import Image
#import argparse
#import cv2
from datetime import datetime

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

def createnewroom(fs, db, file, name):
    with open(file, 'rb') as f:
        image = f.read()
        imageID = fs.put(image, filename=file)

    newrooms = Room(fs, name, file)
    db.insert_one(newrooms.__dict__)
    return 

def findroomlist(db, name):
    return db.find({"room_name": name})

def findroomone(db, name):
    return db.find_one({"room_name": name})

def loadroomimage(fs, room, writename=None):
    file = fs.find_one({'filename': room["location"]})
    image = file.read()
    if writename is not None:
        output = open(writename,"wb") 
        output.write(image)
    return 

time = ["0800", "0830", "0900", "0930", "1000", "1030", "1100", "1130", "1200", "1230", "1300", "1330", "1400", "1430", "1500",
        "1530", "1600", "1630", "1700", "1730", "1800", "1830", "1900", '1930', "2000", "2030", "2100", "2130", "2200"]


def checkavailable(db, name, date, format_data):
    room = db.find_one({"_id": name})
    day = room["available"]
    # available = room["available"]
    # db.update({'filename': room["location"]}, {})
    if day.get(date) is None:
        day[date] = []
        db.update_one({"_id": name}, {'$set': {'available': day}})
    # daytime = room["available"].get(date) 
    for t in time:
        if t in day[date]: continue
        time_data = date + " " + t[:2] + ':' + t[2:] + ':00'
        # print(time_data)
        print(datetime.strptime(time_data, format_data))

def bookroom(db, name, date, format_data):
    checkavailable(db, roomone['_id'], time_data, format_data)
    room = db.find_one({"_id": name})
    day = room["available"]
    ft, tt, user = map(str, input("from time & to time & use id: 0800 0900 ust.hk\n").split())
    for i in range(time.index(ft), time.index(tt)):
        if time[i] in day[date]: 
            print("Not Available Time")
            return 
    for i in range(time.index(ft), time.index(tt)): day[date].append(time[i])
    db.update_one({"_id": name}, {'$set': {'available': day}})
    booking = room['booking']
    if booking.get(user) is None: 
        booking[user] = [[ft, tt]]
        db.update_one({"_id": name}, {'$set': {'booking': booking}})
    else:
        booking[user].append([[ft, tt]])
        db.update_one({"_id": name}, {'$set': {'booking': booking}})
    return 

if __name__ == '__main__':
    # args = get_parser()
    db = connection("AVATA")
    rooms = db['rooms']
    fs = gridfs.GridFS(db)

    createnewroom(fs, rooms, 'ieda.jpg', ["IEDA Conference Room", "5554"])

    # roomlist = findroomlist(rooms, "5554")
    roomone = findroomone(rooms, "5554")
    # roomone = roomlist[0]

    loadroomimage(fs, roomone, "test.jpg")

    time_data = input("Date to book: 2022/04/20\n")
    format_data = "%Y/%m/%d %H:%M:%S"
    # checkavailable(rooms, roomone['_id'], time_data, format_data) # datetime.strptime(time_data, format_data)
    bookroom(rooms, roomone['_id'], time_data, format_data)
    checkavailable(rooms, roomone['_id'], time_data, format_data)


    # newacconts = Account("test@ust.hk", "4223")
    # accounts.insert_one(newacconts.__dict__)