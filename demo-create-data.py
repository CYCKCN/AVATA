import os
import json

import img_trans

ROOT=os.getcwd()
if not os.path.exists(os.path.join(ROOT,'_temp')):
    os.mkdir(os.path.join(ROOT,'_temp'))

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

read=open('demo-data.json','r')
data=json.load(read)


mac=data['mac']
win=data['win']
none_=data['none']

personal=[mac,win,none_]

with open(os.path.join(PATH_2,'_.txt'),'w') as f:
    for i in range(len(mac)):
        type_=mac[str(i)]['type']
        img=mac[str(i)]['image']
        text=mac[str(i)]['text']
        for j in range(len(img)):
            img_trans.image_decoder(img[str(j)],os.path.join(PATH_2,f"_{i}_{j}_{type_}"))
            f.write(f"_{i}_{j}_ ")
            f.write(text[str(j)])
            f.write('\n')


with open(os.path.join(PATH_3,'_.txt'),'w') as f:
    for i in range(len(win)):
        type_=win[str(i)]['type']
        img=win[str(i)]['image']
        text=win[str(i)]['text']
        for j in range(len(img)):
            img_trans.image_decoder(img[str(j)],os.path.join(PATH_3,f"_{i}_{j}_{type_}"))
            f.write(f"_{i}_{j}_ ")
            f.write(text[str(j)])
            f.write('\n')


with open(os.path.join(PATH_4,'_.txt'),'w') as f:
    for i in range(len(none_)):
        type_=none_[str(i)]['type']
        img=none_[str(i)]['image']
        text=none_[str(i)]['text']
        for j in range(len(img)):
            img_trans.image_decoder(img[str(j)],os.path.join(PATH_4,f"_{i}_{j}_{type_}"))
            f.write(f"_{i}_{j}_ ")
            f.write(text[str(j)])
            f.write('\n')

