import os
import json

ROOT=os.getcwd()

PATH_1=os.path.join(ROOT,'_temp','demo-data')
PATH_2=os.path.join(PATH_1,'mac')
PATH_3=os.path.join(PATH_1,'win')
PATH_4=os.path.join(PATH_1,'none')

if not os.path.exists(PATH_1):
    os.mkdir(PATH_1)

if not os.path.exists(PATH_2):
    os.mkdir(PATH_2)

if not os.path.exists(PATH_3):
    os.mkdir(PATH_3)

if not os.path.exists(PATH_4):
    os.mkdir(PATH_4)

read=open('data.json','r')
data=json.load(read)

print(type(data))
