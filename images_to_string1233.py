
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
import bs4
from io import BytesIO
import requests
import database_connection



#System path for tesseract.exe
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'



def img_url(column_name,table_name,id_article):
    img_url_list=[]
    post_id_list=[]
    posts_list=database_connection.connect(column_name,table_name)
    for i in range(len(posts_list)):
    	user_post=posts_list[i]
    	soup = bs4.BeautifulSoup(user_post, "html.parser")
    	images = soup.findAll('img')
    	for image in images:
    		img_url_list.append(str(image['src']))
    		post_id_list.append(id_article[i])


    return img_url_list,post_id_list



#len(articles_images_url_list)

def text_from_article_images(articles_images_url_list,post_id_list):
	'''
	Function for extracting text from images inside Description of article

		parameters:
			list of all urls of images,Ids of corresponding post
	
	'''

	for i in range(10):
	    im=str(articles_images_url_list[i])
	    id_no=post_id_list[i]
	    print(im)
	    print('Id in database is ',id_no)
	    if im.startswith('http'):
	        response = requests.get(im)

	        try:
	            img = Image.open(BytesIO(response.content))
	            text=pytesseract.image_to_string(img,lang='eng')
	            plt.imshow(img)
	            plt.show(img)
	            print(text)
	            print('-'*50)

	        except Exception as e:
	            print('Skipping ', i)
	            print('Exception found ',e)
	            print("Status code",response.status_code)
	            print('-'*50)
	            i+=1
	            continue
	    else:
	        print('Invalid url')
	        print('-'*50)
	        continue
        

def preprocess_profile_images(profile_img_url_list,id_article):
	'''
	This function preprocesses all the profile_images by removing irrelevant spaces and adding a specific prefix
	

		Parameters:
			list of all profile images present inside database,id of article
		Return:
			list of all processed images url,list of profile ids corresponding to that article
	'''
	profile_img_list=[]
	profile_id_list=[]
	for j in range(len(profile_img_url_list)):
		i=profile_img_url_list[j]
		i=i.replace(' ','')
		if len(i) is not 0:
			p='https://s3.ap-south-1.amazonaws.com/atg-storage-s3/assets/Frontend/images/article_image/'+str(i)
			profile_img_list.append(p)
			profile_id_list.append(id_article[j])

	#print('list for profile images\n\n ',profile_img_list)
	return profile_img_list,profile_id_list


def text_from_profile_images(profile_img_list,profile_id_list):
	'''
	This funciton extract text from Article Profile images
	'''

	for i in range(10): # for now keeping it as 10
	    im=str(profile_img_list[i])
	    
	    print(im)
	    print("Id of profile is ",profile_id_list[i])
	    response = requests.get(im)

	    try:
	        img = Image.open(BytesIO(response.content))
	        text=pytesseract.image_to_string(img,lang='eng')
	        plt.imshow(img)
	        plt.show(img)
	        print(text)
	        print('-'*50)

	    except Exception as e:
	        print('Skipping ', i)
	        print('-'*50)
	        i+=1
	        continue


id_article=database_connection.connect('id,profile_image','p1036_mst_article')

#Requesting database for Description column and extracting images url 
articles_images_url_list,post_id_list=img_url('description','p1036_mst_article',id_article)

#Extracting text from images present inside the article
text_from_article_images(articles_images_url_list,post_id_list)

#Requesting database for profile images of article 
profile_img_url_list=database_connection.connect('profile_image','p1036_mst_article')

profile_img_list,profile_id_list=preprocess_profile_images(profile_img_url_list,id_article)

#Extracting text from profile images
text_from_profile_images(profile_img_list,profile_id_list)





