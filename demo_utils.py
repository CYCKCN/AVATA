import os
import json
from queue import Queue
from flask import url_for


def create_queue(root,personal='win'):
    path=os.path.join(root,'frontend','static','_temp','demo-data',personal)
    file=os.listdir(path)

    txt_file=open(os.path.join(path,file[0]),'r')
    txt=txt_file.read()
    txt_file.close()

    txt=txt.split('\n')
    txt_=[]
    for i in range(len(txt)):
        if txt[i]=='': continue
        t=txt[i].split('_ ')
        txt_.append(t[1])
    
    img_=[]
    type_=[]
    for i in range(1,len(file)):
        img_.append(os.path.join(path,file[i]))
        if '.mp4' in file[i]: type_.append('video')
        else: type_.append('image')

    cur_step=0
    guide={}
    q=[]
    for i in range(1,len(file)):
        #print(guide)
        #print(file[i].split('_')[1])
        if not file[i].split('_')[1] == str(cur_step):
            cur_step+=1
            q.append(guide.copy())
            guide={}
        #print(f'_temp/demo-data/{personal}/{file[i]}')
        #guide[txt_[i]]=url_for('static',filename='_temp/demo-data/{}/{}'.format(personal,file[i]))
        guide[txt_[i-1]]=url_for('static',filename='_temp/demo-data/'+personal+'/'+file[i])
        #guide[txt_[i-1]]=img_[i-1]

        '''
        if file[i].split('_')[1] == str(cur_step):
            guide[type_[i]]=url_for('static',filename=f'_temp/demo-data/{personal}/{file[i]}')
        else:
            cur_step+=1
            q.put(guide)
            guide={}
        '''
    q.append(guide.copy())
    return q


if __name__ == '__main__':
    q=create_queue(os.getcwd(),'win')
    print(q)


