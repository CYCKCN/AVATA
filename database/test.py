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
    accounts = db["accounts"]

    newacconts = Account("test@ust.hk", "4223")
    accounts.insert_one(newacconts.__dict__)