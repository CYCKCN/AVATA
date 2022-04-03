import os
import time
from pprint import pprint

from cv2 import line
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
                '''
                pos_guide=0
                g={}

                
                for j in range(pos_line,len(lines)):
                    device_name=lines[j].split('_')[0]
                    guide_name=lines[j].split('_')[1]
                    image=lines[j].split(' ')[0]
                    text=lines[j].split(' ')[1]
                    if device_name == self.choose[i]:
                        if not guide_name == 'guide'+str(pos_guide+1):
                            pos_guide+=1
                            pprint(g)
                            guide[len(guide)]={
                                'finish':0,
                                'guide':g.copy()
                            }
                            g={}
                        g[text]=url_for('static',
                        filename='images/test/'+self.room_id+'/'+p+'/'+image+'.png')\
                            if not self.__debug else 'images/test/'+self.room_id+'/'+p+'/'+image+'.png'

                    else: 
                        print(device_name)
                        pos_line=j
                        break
                pprint(g)
                guide[len(guide)]={
                    'finish':0,
                    'guide':g.copy()
                }
                '''
                cur_device_guide=[]
                for j in range(len(lines)):
                    device_name=lines[j].split('_')[0]
                    if device_name==self.choose[i]:
                        cur_device_guide.append(lines[j])
                step_num=int(cur_device_guide[-1].split('_')[1].replace('guide',''))

                for j in range(step_num):
                    g={}
                    for k in range(len(cur_device_guide)):
                        cur_name=int(cur_device_guide[k].split('_')[1].replace('guide',''))
                        if cur_name==j+1:
                            image=cur_device_guide[k].split(' ')[0]
                            text=cur_device_guide[k].split(' ')[1]
                            g[text]=url_for('static',
                            filename='images/test/'+self.room_id+'/'+p+'/'+image+'.png')\
                                if not self.__debug else 'images/test/'+self.room_id+'/'+p+'/'+image+'.png'
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
    choose_devices=room.get_data_personal_device(['win','mac'])
    #pprint(choose_devices)
    _s=time.time()
    guides=room.set_data_instruction()
    _e=time.time()-_s
    pprint(guides)
    print(_e)


    