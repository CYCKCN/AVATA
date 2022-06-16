import argparse
from select import select
from unicodedata import name
import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from object import Account, Device, Controller

def connection(dbname):
    # mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true"&"w=majority
    addr = "mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(addr)
    db = client[dbname]
    return db

def setup_selectdevices(db, selectdevices):
    devices = db["devices"]
    controllers = db["controllers"]

    for dname in selectdevices:
        query = {"name": dname}
        dev = devices.find(query)
        

if __name__ == '__main__':
    # args = get_parser()
    db = connection("AVATA")

    selectdevices = ["projector1", "screen1", "personalmac"]
