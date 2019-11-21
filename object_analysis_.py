'''
This script checks for objects found in an image, it uses yolo for object identification
usage:
just pass the url in findobjectfromcover and decription in findobjectfromcover. it'll print the set of objects found inside that image
'''
import urllib.request
import bs4
import traceback
from darkflow.net.build import TFNet
import cv2
import os
options = {"model": "cfg/yolov2.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

tfnet = TFNet(options)
def img_url(post):
    img_url_list=list()
    #posts_list=database_connection.connect_2_col('id,description','p1036_mst_article')
    #posts_list=user_posts('description','p1036_mst_article')
    #print(posts_list[:25])
    #for user_post in posts_list:
    soup = bs4.BeautifulSoup(post, "html.parser")
    images = soup.findAll('img')
    for image in images:
        '''
        removing faulty links
        '''
        if 'atg.world' in str(image['src']) or str(image['src']).startswith('file:') or str(image['src']).endswith('.gif'):
            pass
        else:
            img_url_list.append(str(image['src']))
    return img_url_list

def findobjectsfrompost(user_post):#pass description
    img_l=img_url(user_post)
    for img in img_l:
    #num+=1
        try:    
            '''
            saving the image in current folder'''
            urllib.request.urlretrieve(img, img.split('/')[-1])

            imgcv = cv2.imread(img.split('/')[-1])
            result = tfnet.return_predict(imgcv)
            objects=list()

            for things in result:
                if things['confidence']>0.57:
                    '''
                    setting the confidence 57%
                    '''
                    objects.append(things['label'])
                #print(things['label'])
            myset=set(objects)
            if myset != set():
                print(str(myset))
            else:
                print("can't find any object")
            #current_res=result[i]
            #next_res=result[i+1]
            #if current_res['label']!=next_res['label']:
             #   print('Label-->%s'%current_res['label'])
                #print('Confidence-->%s'%current_res['confidence'])
            os.remove(img.split('/')[-1])
        except Exception as e:
            pass
        #traceback.print_exc()
        #print(img)#print(db_conn.img_url())
def findobjectsfromcover(cover_url):#pass full url with http 
    #num+=1
    try:    
        '''
            saving the image in current folder'''
        urllib.request.urlretrieve(cover_url, cover_url.split('/')[-1])
        imgcv = cv2.imread(cover_url.split('/')[-1])
        result = tfnet.return_predict(imgcv)
        objects=list()
        for things in result:
            if things['confidence']>0.57:#confidence set to 57%
                objects.append(things['label'])
            #print(things['label'])
        myset=set(objects)
        if myset != set():
            print(str(myset))
        else:
            print("can't find any object")
            #current_res=result[i]
            #next_res=result[i+1]
            #if current_res['label']!=next_res['label']:
             #   print('Label-->%s'%current_res['label'])
                #print('Confidence-->%s'%current_res['confidence'])
        os.remove(cover_url.split('/')[-1])
    except Exception as e:
        pass
        #traceback.print_exc()
        #print(img)#print(db_conn.img_url())
'''
examples given below->'''
#findobjectsfrompost('<p>The eyes of skies when filled up with the tears,</p><p>Dark clouds like eyelids cover its alluring blue color.</p><p>The Subtle winds swirls into usher in the showers of dismal,</p><p>Dropping out the thick teardrops that accompanied with thunder screams,<span style="background-color: initial;">Just with the celestial intervention.</span></p><p><span style="background-color: initial;"><img class="fr-dib fr-draggable" src="https://s3.ap-south-1.amazonaws.com/atg-test-s3/assets/Backend/img/group_img/cover/Adventure.jpg"></span><br></p><p>The breezy sky with the drop of the tear,</p><p><span style="background-color: initial;">The blazing of a fiercy ball pierced through the dark skies,</span></p><p>Glowing with the rainy drops, to reflect the colorful sky.</p><p>The shyness of the rainbow is in the love with sky, coming out with the colors just to make the people in love with the sky.</p><p>Colors of Rainbow make both of them not to cry, the teary eyes though fell in love with the colorful sky.</p>')
#findobjectsfromcover('https://s3.ap-south-1.amazonaws.com/atg-test-s3/assets/Backend/img/group_img/cover/Adventure.jpg')