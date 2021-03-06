from calendar import calendar, monthrange
import os
import time
import gridfs
import cv2 as cv
from pprint import pprint
from datetime import datetime

from cv2 import line
from flask import Blueprint, render_template, redirect, url_for, request

import database.booking as room_booking

PERSONAL_TYPE=['mac','win','none']
MONTH_ABBR={
    1:'Jan',
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'June',
    7:'July',
    8:'Aug',
    9:'Sept',
    10:'Oct',
    11:'Nov',
    12:'Dec'
}
WEEK_ABBR={
    0:'Mon',
    1:'Tue',
    2:'Wed',
    3:'Thu',
    4:'Fri',
    5:'Sat',
    6:'Sun'
}

class ROOM:
    def __init__(self,debug=False,oscwd=os.getcwd()):
        self.oscwd=oscwd
        self.__debug=debug
        self.ROOT=''
        self.room_id=''
        self.user=''

        self.image_360=None
        self.image_360_deivces=None
        self.image_360_deivces_related=None

        self.choose=None
        self.choose_devices=None
        self.choose_personal=None

        self.choose_devices_related=None

        self.guides=None

        self.guide_queque=[]
        self.guide_device=None
        self.guide_queque_size=0
        self.guide_device_order=None

        self.db=room_booking.connection("AVATA")
        self.fs=gridfs.GridFS(self.db)
        self.db_roomone=None

        self.today_date=\
            list(map(int,(datetime.today().strftime('%Y %m %d')+' '+str(datetime.today().weekday())).split(' ')))
        self.booking_week=None
        self.booking_time=[t[:2]+' : '+t[2:] for t in room_booking.time]
        self.booking_occupy=None
        self.booking_access_date=[]
        self.booking_result=None

    def __call__(self, room_id='room1', user='test'):
        self.ROOT=os.path.join(self.oscwd,'frontend','static','images','test',room_id)
        self.user=user
        
        self.room_id=room_id

        self.image_360=url_for('static',filename='images/test/'+room_id+'/360-1.jpg')\
                        if not self.__debug else 'images/test/'+room_id+'/360-1.jpg'
        self.image_360_deivces=None
        self.image_360_deivces_related=None

        self.choose=None
        self.choose_devices=None
        self.choose_personal=None

        self.choose_devices_related=None

        self.guides=None

        self.guide_queque=[]
        self.guide_device=None
        self.guide_queque_size=0
        self.guide_device_order=None

        self.db_roomone=room_booking.findroomone(self.db['rooms'], room_id)
        self.booking_occupy=None


    def __read_360_txt(self,path):
        lines=[]
        f = open(path)
        for line in f:
            lines.append(line.replace('\n',''))
        f.close()
        return lines

    def __read_guide_txt(self):
        L={}
        for p in self.choose_personal:
            root=os.path.join(self.ROOT,p,'text.txt')
            lines=[]
            f = open(root)
            for line in f:
                if line.split('_')[0] in self.choose:
                    lines.append(line.replace('\n',''))
            f.close()
            L[p]=lines
        return L

    def create_guide_queue(self,device):
        self.guide_device=device
        g=self.guides[device]
        q=[]
        for _, d in g.items():
            q.append(d['guide'])
        self.guide_queque=q
        self.guide_queque_size=len(q)

        for _, d in self.choose_devices_related.items():
            if d['name']==device:
                d['clicked']='y'

    def pop_guide_queue(self):
        index=self.guide_queque_size-len(self.guide_queque)
        self.guides[self.guide_device][index]['finish']=1
        return self.guide_queque.pop(0)

    def choose_devices_relative(self,use_related=True):
        if not self.choose_devices_related==None:
            return self.choose_devices_related

        img=cv.imread(os.path.join(self.ROOT,'360.png'))
        V, U, _=img.shape
        devices={}
        for i,_d in self.choose_devices.items():
            device={}
            d=_d.copy()
            device['name']=d['name']
            if use_related:
                device['v']=str(int(int(d['v'].replace('px',''))/V*100))+'%'
                device['u']=str(int(int(d['u'].replace('px',''))/U*100))+'%'
            else:
                device['v']=d['v']
                device['u']=d['u']
            device['clicked']='n'
            devices[i]=device
        self.choose_devices_related=devices
        return devices

    def set_data_choose_devices(self,use_related=False):#database->devices.html
        root=os.path.join(self.ROOT,'360.txt')
        lines=self.__read_360_txt(root)
        devices={}
        for i in range(len(lines)):
            device={}
            line=lines[i].split(' ')
            device['name']=line[0]
            device['v']=line[1]+'px'
            device['u']=line[2]+'px'
            devices[i]=device
        self.image_360_deivces=devices

        img=cv.imread(os.path.join(self.ROOT,'360.png'))
        V, U, _=img.shape
        devices_related={}
        for i in range(len(lines)):
            device_related={}
            line=lines[i].split(' ')
            device_related['name']=line[0]
            device_related['v']=str(int(int(line[1])/V*100))+'%'
            device_related['u']=str(int(int(line[2])/U*100))+'%'
            devices_related[i]=device_related
        self.image_360_deivces_related=devices_related

        if use_related:
            return devices_related
        else:
            return devices

    def get_data_choose_devices(self):#devices.html->database
        choose=[]
        for _, d in self.image_360_deivces.items():
            if request.form.get(d['name']):
                choose.append(request.form.get(d['name']))
        self.choose=choose
        self.guide_device_order=choose

    def get_data_personal_device(self,personal):#personal-device.html->database
        self.choose_personal=personal
        choose_devices={}
        for i, d in self.image_360_deivces.items():
            if d['name'] in self.choose:
                choose_devices[len(choose_devices)]=self.image_360_deivces[i]
        self.choose_devices=choose_devices
        #return choose_devices

    def set_data_instruction(self):#database->instruction(-choose).html
        #root=os.path.join(self.ROOT,self.choose_personal,'text.txt')
        #lines=self.__read_guide_txt()
        #print(lines)
        L=self.__read_guide_txt()
        #pprint(L)
        guides={}
        #pos_line=0
        for i in range(len(self.choose)):
            guide={}
            for p, lines in L.items():
                cur_device_guide=[]
                for j in range(len(lines)):
                    device_name=lines[j].split('_')[0]
                    if device_name==self.choose[i]:
                        cur_device_guide.append(lines[j])
                step_num=int(cur_device_guide[-1].split('_')[1].replace('guide',''))

                for j in range(step_num):
                    g={}
                    g_index=0
                    for k in range(len(cur_device_guide)):
                        cur_name=int(cur_device_guide[k].split('_')[1].replace('guide',''))
                        if cur_name==j+1:
                            name=cur_device_guide[k].split(' ')[0]
                            text=cur_device_guide[k].split(' ')[1]
                            file_type=cur_device_guide[k].split(' ')[2]
                            if file_type=='video': name=name+'.mp4'
                            else: name=name+'.png'
                            g[g_index]={
                                'text':text,
                                'type':file_type,
                                'name':url_for('static',
                                    filename='images/test/'+self.room_id+'/'+p+'/'+name)\
                                    if not self.__debug else 'images/test/'+self.room_id+'/'+p+'/'+name
                            }
                            g_index+=1
                            '''
                            g[text]=url_for('static',
                            filename='images/test/'+self.room_id+'/'+p+'/'+image+'.png')\
                                if not self.__debug else 'images/test/'+self.room_id+'/'+p+'/'+image+'.png'
                            '''
                            
                    guide[len(guide)]={
                        'finish':0,
                        'guide':g.copy()
                    }

            guides[self.choose[i]]=guide.copy()
        self.guides=guides
        return guides, self.choose_devices
    
    def set_guide_order(self,order):
        self.guide_device_order=order

    def get_guide_order(self):
        text=''
        for i, d in enumerate(self.guide_device_order):
            text+=d
            if not i+1==len(self.guide_device_order):
                text+=' -> ' 

        return text

    def set_booking_week(self):
        booking={}
        _,month_days=monthrange(self.today_date[0],self.today_date[1])
        for i in range(7):
            week=(self.today_date[3]+i)%7
            day=self.today_date[2]+i
            if day>month_days: day=day-month_days
            booking[WEEK_ABBR[week]]=day

            if self.today_date[2]+i>month_days: #didn't consider next year
                date="{:d}/{:0>2d}/{:0>2d}".format(self.today_date[0],
                    self.today_date[1]+1,
                    self.today_date[2]+i-month_days)
            else:
                date="{:d}/{:0>2d}/{:0>2d}".format(self.today_date[0],
                    self.today_date[1],
                    self.today_date[2]+i)
            self.booking_access_date.append(date)

        self.booking_week=booking

        return booking

    def set_booking_occupy(self):
        occupy={}
        name=self.db_roomone['_id']
        room = self.db['rooms'].find_one({"_id": name})
        day = room["available"]

        for t in room_booking.time:
            for d in self.booking_access_date:
                _t=t[:2]+' : '+t[2:]
                _d=int(d.split('/')[2])
                if not day.get(d) is None and t in day[d]:
                    occupy[(_t,_d)]='y'
                else:
                    occupy[(_t,_d)]='n'
        
        self.booking_occupy=occupy
        return occupy

    def get_booking_result(self):
        for k, v in self.booking_occupy.items():
            t,d=k
            if v=='y': continue
            if request.form.get(f"time-{d}-{t}"):
                time_data="{:d}/{:0>2d}/{:0>2d}".format(self.today_date[0],self.today_date[1],d)
                clock=t.replace(' : ','')
                self.db_bookroom(self.db['rooms'],self.db_roomone['_id'],time_data,clock)

    def db_bookroom(self, db, name, date, clock, format_data="%Y/%m/%d %H:%M:%S"):
        time=room_booking.time
        room_booking.checkavailable(db, self.db_roomone['_id'], date, format_data)
        room = db.find_one({"_id": name})
        day = room["available"]
        #ft, tt, user = map(str, input("from time & to time & use id: 0800 0900 ust.hk\n").split())
        ft=clock
        tt=time[time.index(ft)+1]
        user=self.user
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
    '''
    lines=[]
    ROOT=os.path.join(os.getcwd(),'frontend','static','images','test','room1')
    path=os.path.join(ROOT,'360.txt')
    f = open(path)
    for line in f:
        lines.append(line.replace('\n',''))
    #print(lines)
    devices={}
    for i in range(len(lines)):
        device={}
        line=lines[i].split(' ')
        device['name']=line[0]
        device['v']=line[1]+'px'
        device['u']=line[2]+'px'
        devices[i]=device
    #print(devices)
    
    choose_devices={}
    choose=['device001','device003']
    for i, d in devices.items():
        if d['name'] in choose:
            choose_devices[len(choose_devices)]=devices[i]
    choose_devices=choose_devices
    print(choose_devices)
    root=os.path.join(ROOT,'mac','text.txt')
    lines=[]
    f = open(root)
    for line in f:
        if line.split('_')[0] in choose:
            lines.append(line.replace('\n',''))
    print(lines)
    '''
    room=ROOM(debug=True)
    room('room1')
    #print(room.image_360)
    devices=room.set_data_choose_devices()
    #pprint(devices)
    room.choose=['device001','device002','device004']
    choose_devices=room.get_data_personal_device(['win','mac'])
    #pprint(choose_devices)
    _s=time.time()
    guides=room.set_data_instruction()
    _e=time.time()-_s
    pprint(guides)
    print(_e)

    #print(room.choose_devices_relatedrelative())
    room.create_guide_queue('device001')
    pprint(room.guide_queque)
    print('')
    pprint(room.pop_guide_queue())
    print('')
    pprint(room.guides)
    