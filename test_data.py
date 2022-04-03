import os
from pprint import pprint
from posixpath import devnull
from queue import Queue
from flask import Blueprint, render_template, redirect, url_for, request

class ROOM:
    def __init__(self,room_id='room1'):
        self.__debug=False

        self.ROOT=os.path.join(os.getcwd(),'frontend','static','images','test',room_id)
        self.room_id=room_id

        self.image_360=url_for('static',filename='images/test/'+room_id+'/360.png')\
                        if not self.__debug else 'images/test/'+room_id+'/360.png'
        self.image_360_deivces=None

        self.choose=None
        self.choose_devices=None
        self.choose_personal=None

        self.guides=None

    def __read_360_txt(self,path):
        lines=[]
        f = open(path)
        for line in f:
            lines.append(line.replace('\n',''))
        return lines

    def __read_guide_txt(self,path):
        lines=[]
        f = open(path)
        for line in f:
            if line.split('_')[0] in self.choose:
                lines.append(line.replace('\n',''))
        return lines

    def set_data_choose_devices(self):#database->devices.html
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
        return devices

    def get_data_choose_devices(self,request):#devices.html->database
        choose=[]
        for _, d in self.image_360_deivces.items():
            if request.form.get(d['name']):
                choose.append(request.form.get(d['name']))
        self.choose=choose

    def get_data_personal_device(self,personal):#personal-device.html->database
        self.choose_personal=personal
        choose_devices={}
        for i, d in self.image_360_deivces.items():
            if d['name'] in self.choose:
                choose_devices[len(choose_devices)]=self.image_360_deivces[i]
        self.choose_devices=choose_devices
        return choose_devices

    def set_data_instruction(self):#database->instruction(-choose).html
        root=os.path.join(self.ROOT,self.choose_personal,'text.txt')
        lines=self.__read_guide_txt(root)
        #print(lines)
        guides={}
        pos_line=0
        for i in range(len(self.choose)):
            pos_guide=0
            guide={}
            g={}
            for j in range(pos_line,len(lines)):
                device_name=lines[j].split('_')[0]
                guide_name=lines[j].split('_')[1]
                image=lines[j].split(' ')[0]
                text=lines[j].split(' ')[1]
                if device_name == self.choose[i]:
                    if not guide_name == 'guide'+str(pos_guide+1):
                        pos_guide+=1
                        guide[len(guide)]={
                            'finish':0,
                            'guide':g.copy()
                        }
                        g={}
                    g[text]=url_for('static',
                    filename='images/test/'+self.room_id+'/'+self.choose_personal+'/'+image+'.png')\
                        if not self.__debug else 'images/test/'+self.room_id+'/'+self.choose_personal+'/'+image+'.png'

                else: 
                    pos_line=j
                    break
            guide[len(guide)]={
                'finish':0,
                'guide':g.copy()
            }
            guides[self.choose[i]]=guide.copy()
        self.guides=guides
        return guides

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
    room=ROOM('room1')
    #print(room.image_360)
    devices=room.set_data_choose_devices()
    #pprint(devices)
    room.choose=['device001','device002','device004']
    choose_devices=room.get_data_personal_device('win')
    #pprint(choose_devices)
    guides=room.set_data_instruction()
    pprint(guides)

    