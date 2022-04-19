import os
import time
import cv2 as cv
from pprint import pprint

from cv2 import line
from flask import Blueprint, render_template, redirect, url_for, request

PERSONAL_TYPE=['mac','win','none']

class ROOM:
    def __init__(self,debug=False,oscwd=os.getcwd()):
        self.oscwd=oscwd
        self.__debug=debug
        self.ROOT=''
        self.room_id=''

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
    
    def __call__(self, room_id='room1'):
        self.ROOT=os.path.join(self.oscwd,'frontend','static','images','test',room_id)
        
        self.room_id=room_id

        self.image_360=url_for('static',filename='images/test/'+room_id+'/mid.png')\
                        if not self.__debug else 'images/test/'+room_id+'/mid.png'
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

    def choose_devices_relative(self):
        if not self.choose_devices_related==None:
            return self.choose_devices_related

        img=cv.imread(os.path.join(self.ROOT,'360.png'))
        V, U, _=img.shape
        devices={}
        for i,_d in self.choose_devices.items():
            device={}
            d=_d.copy()
            device['name']=d['name']
            device['v']=str(int(int(d['v'].replace('px',''))/V*100))+'%'
            device['u']=str(int(int(d['u'].replace('px',''))/U*100))+'%'
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
    