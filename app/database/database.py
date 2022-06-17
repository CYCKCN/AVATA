import argparse
from unicodedata import name
import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from db import AccountDB, DeviceDB, RoomDB
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

    accountdb = AccountDB(db)
    devicedb = DeviceDB(db)
    roomdb = RoomDB(db)
    
    # devices = db["devices"]
    # controllers = db["controllers"]
    # fs = GridFS(db)
    # file = "ieda.jpg"
    # with open(file, 'rb') as f:
    #     image = f.read()
    # stored = fs.put(image, filename='files')

    