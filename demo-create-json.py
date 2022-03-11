import json
from pprint import pprint
from easydict import EasyDict

import img_trans

#img_trans.image_encoder('')
room = {
    'id':'IEDA Conference Room',
    'image-room':img_trans.image_encoder('frontend\static\images\demo-ieda\\360-2.JPG'),
    'image-360':img_trans.image_encoder('frontend\static\images\demo-ieda\\360-1.JPG'),
    'mac':{
        0:{
            'title':'Control Box',
            'image':{
                0:img_trans.image_encoder('frontend\static\images\demo-ieda\Macbook\Control-Box-1.jpeg'),
                1:img_trans.image_encoder('frontend\static\images\demo-ieda\Macbook\Control-Box-2.jpeg'),
                2:img_trans.image_encoder('frontend\static\images\demo-ieda\Macbook\Control-Box-3.jpeg')
            },
            'text':{
                0:'Find the control box on the lectern and press “System On”',
                1:'Select as shown in the picture (the projector needs time to be ready, please wait)',
                2:'Continue to set up at your Apple laptop'
            },
            'type':'.jpg'
        },
        1:{
            'title':'Apple',
            'image':{
                0:img_trans.image_encoder('frontend\static\images\demo-ieda\Macbook\Apple-1.mp4'),
                1:img_trans.image_encoder('frontend\static\images\demo-ieda\Macbook\Apple-2.mp4')
            },
            'text':{
                0:'Select “Screen Mirroring” - “ielm conference”',
                1:'Enter the AirPlay code'
            },
            'type':'.mp4'
        }
    },
    'win':{
        0:{
            'title':'Lectern',
            'image':{
                0:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Lectern-1.jpeg'),
                1:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Lectern-2.jpeg'),
                2:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Lectern-3.jpeg')
            },
            'text':{
                0:'Find the control box on the lectern and press “System On”',
                1:'Select as shown in the picture (the projector needs time to be ready, please wait)',
                2:'Continue to set up at the conference table'
            },
            'type':'.jpg'
        },
        1:{
            'title':'Conference Table',
            'image':{
                0:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Conference-Table-1.jpeg'),
                1:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Conference-Table-2.JPG'),
                2:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Conference-Table-3.jpeg'),
                3:img_trans.image_encoder('frontend\static\images\demo-ieda\Windows laptop\Conference-Table-4.jpeg')
            },
            'text':{
                0:'Find the HDMI cable underneath the conference table',
                1:'Plug the HDMI cable into your laptop',
                2:'Press “Fn” and “F7” on your laptop',
                3:'Select “Duplicate” on the pop-up window'
            },
            'type':'.jpg'
        }
    },
    'none':{
        0:{
            'title':'Guide',
            'image':{
                0:img_trans.image_encoder('frontend\static\images\demo-ieda\\None\p1.jpg'),
                1:img_trans.image_encoder('frontend\static\images\demo-ieda\\None\p2.jpg'),
                2:img_trans.image_encoder('frontend\static\images\demo-ieda\\None\p3.jpg')
            },
            'text':{
                0:'Find the control box on the lectern and press “System On”',
                1:'Select as shown in the picture (the projector needs time to be ready, please wait)',
                2:'The devices are ready for your presentation'
            },
            'type':'.jpg'
        },
    }
}

out = open('demo-data.json','w')
json.dump(room,out)



