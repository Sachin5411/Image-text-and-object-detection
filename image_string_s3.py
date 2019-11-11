'''
This is the main Script 
	->It is responsible for  
		->Extacting text from images 
		->Finding out the Objects in a image (using script object_analysis_.py)
		->Finding if the description provided is Business post or Not (using script business_model.py)
		->Finding if the post is abusive or not(using script abuse.py)
		->Finding the post context (using script post_contexts.py)
		-> Spam analysis (using script spammer.py) PS:- spammer.py needs to be run separately

	NOTE:
		To run the script you need to provide required arguments
		MAKE SURE THERE ARE NO DOUBLE QUOTES("") IN BETWEEN THE DESCRIPTION ....CONVERT THEM INTO SINGLE QUOTES('') (IF THERE ARE ANY)
		PS:- SOME SAMPLE DESCRIPTIONS ARE PROVIDED AT THE END OF THIS SCRIPT

'''

import argparse
import boto3
from pymemcache.client import base
import os
import json
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
from io import BytesIO
import requests
import bs4
import re
from bs4 import BeautifulSoup
import abuse
import business_model
import post_contexts
import database_connection
import spam_filter
# import object_analysis_


#System path for tesseract.exe
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


ap = argparse.ArgumentParser()

ap.add_argument('-u', '--user_id',type=int,
	help='user id (int )')
ap.add_argument('-f', '--feature',
	help='string type')
ap.add_argument('-fid', '--feature_id',
	help='int type')
ap.add_argument('-t', '--title',
	help='string type')
ap.add_argument('-d', '--description',
	help='string type')
ap.add_argument('-c', '--cover_image',
	help='string type')
ap.add_argument('-tag', '--tags',
	help='comma separated string')
ap.add_argument('-g', '--group_id')
args = vars(ap.parse_args())


#Caching the data provided for 7 days
# print("Caching the details provided in the arguments........")
# data={ "user_id":args['user_id'],"feature":args['feature'],"title":args['title'],"description":args['description'],"cover_img":args['cover_image'],"tag":args['tags'],"group_id":args['group_id'],'feature_id':args['feature_id']}
# #print(json.dumps(data))
# client=base.Client(('localhost',11211))
# if client.get(str(0)) == None:
# 	predefined_groups=database_connection.connect('group_name','p1036_mst_group')
# 	#print(predefined_groups)
# 	client.set(str(0),json.dumps(predefined_groups),expire=172800)
# if client.get(str(args['user_id'])) == None:
#     client.set(str(args['user_id']),json.dumps(data)+'\n',expire=604800)
# else:
#     client.append(str(args['user_id']),json.dumps(data)+'\n')
# print('-'*50)
# print("DONE.........")

# def get_url(image_name):
# 	s3 = boto3.resource('s3')
# 	for obj in s3.Bucket(name='atg-test-s3').objects.all():
# 		if args['feature'] is None:
# 			if image_name in obj.key:
# 				path=obj.bucket_name+'/'+obj.key
# 				print(path)
# 				return 'https://s3.ap-south-1.amazonaws.com/'+path
# 		elif args['feature'] is not None:

# 		    if image_name in obj.key and args['feature'] in obj.key:
# 		        #print(obj.key)
		        
# 		        path=obj.bucket_name+'/'+obj.key
# 		        print(path)
# 		        return 'https://s3.ap-south-1.amazonaws.com/'+path
# 	return 'No such Image'


def images_in_description(description):

	'''
	This function finds out if there are any images in Description and extracts text from them (If found)

		Parameter: Description of Post

	'''
	
	soup = bs4.BeautifulSoup(description, 'html.parser') #creating a beautiful soup object for parsing the description
	images = soup.findAll('img')
	for image in images: #looping all the images found in the description
		print(image['src'])
		if image['src'].startswith('http'):
			response = requests.get(image['src'])
			try:
				img = Image.open(BytesIO(response.content)) #to open the image in byte format
				text=pytesseract.image_to_string(img,lang='eng') #finding text from image
				plt.imshow(img) #Displaying the image
				plt.show(img)
				print(text)
				print('-'*50)
			except Exception as e:
				print('Skipping.... ')
				print('Exception found ',e)
				print('Status code',response.status_code)
				print('-'*50)
				continue

def get_contact_details(description):
	'''
	This Function finds out any phone number or emails present in the description and cached them (If found)

	'''
	#regex for email and phone number
	contact_number=re.findall('|'.join(['\+\d\d?-? ?\d{3}-\d{3}-\d{4}','\\+\\d\\d?-? ?\\d{10}','\\+\\d\\d?-? ?\\d{5} \\d{5}','\\+\\d\\d?-? ?\\d{3}\\-? ?\\d{7}','\\+\\d\\d?-? ?\\d{4}\\-? ?\\d{6}']) ,description)
	email=re.findall('\w+@\w+\.{1}\w+',description)

	if len(contact_number) is not 0:
		print('Phone number found in description ',contact_number)
		#print('Caching the details...')
		print('-'*50)
	if len(email) is not 0:
		print('Email found in the description ',email)
		#print('Caching the details...')
		print('-'*50)

def make_imageurl(im_name,feature):
	'''
	This is a helper function for get_string function ,It converts the image url to complete URL

		Parameters:
			Name of the image , Group(feature) to which the image Belongs to
		Returns:
			Complete URL

	'''
	image_url='https://s3.ap-south-1.amazonaws.com/atg-test-s3/assets/Frontend/images/'+feature+'_image/'+im_name

	return image_url

def get_string(im_name,feature):
	'''
	This function uses function make_imageurl as a helper function to get the full url of the image name provided
	After this, It Extracts the String from the image

		Parameters:
			Name of the image , Group(feature) to which the image Belongs to

	'''
	im=make_imageurl(im_name,feature)
	print('image url ',im)
	if 'atg.world' in str(im) or str(im).startswith('file:') or str(im).endswith('.gif'):
		pass
	else:
		#object_analysis_.findobjectsfromcover(im)
		response = requests.get(im) #sending request for the image
		try:

			img = Image.open(BytesIO(response.content))
			text=pytesseract.image_to_string(img,lang='eng')
			plt.imshow(img)
			plt.show(img)
			print(text)
			print('-'*50)
		except Exception as e:
			print('Exception found ',e)
			print('status code ',response.status_code)



if args['cover_image'] is not None:
	get_string(args['cover_image'],args['feature'])
if args['cover_image'] is None:
	print("It seems like you didn't pass any cover image")
	print('-'*50)
if args['description'] is not None:
	print('FINDING TEXT OF IMAGES IN DESCRIPTION.....')
	images_in_description(args['description'])
	print('-'*50)
	# print('FINDING OBJECTS IN DESCRIPTION IMAGES........')
	# object_analysis_.findobjectsfrompost(args['description'])
	# print('-'*50)
	print('CHECKING FOR ABUSE ........')
	abuse.abusive_analysis(args['description'])
	print('-'*50)
	print('CHECKING FOR SPAM.........')
	spam_filter.spam_group(args['description'])
	print('-'*50)
	print('CHECKING FOR BUSINESS POST...')
	business_model.busi_group(args['description'])
	print('-'*50)
	print('CHECKING FOR CONTACTS IN DESCRIPTION.......')
	get_contact_details(args['description'])
	print('-'*50)
	print('CHECKING FOR POST CONTEXTS.......')
	post_contexts.context_analysis(args['description'])


if args['description'] is None:
	print('It seems like no description provided')
	print('-'*50)



#SOME SAMPLE DESCRIPTIONS ARE SHOWN BELOW


#'''<p>The eyes of skies when filled up with the tears,</p><p>Dark clouds like eyelids cover it's alluring blue color.</p><p>The Subtle winds swirls into usher in the showers of dismal,</p><p>Dropping out the thick teardrops that accompanied with thunder screams,<span style='background-color: initial;'>Just with the celestial intervention.</span></p><p><span style='background-color: initial;'><img class='fr-dib fr-draggable' src='https://s3.ap-south-1.amazonaws.com/atg-test-s3/assets/Backend/img/group_img/cover/Accessories Inventors.jpg'></span><br></p><p>The breezy sky with the drop of the tear,</p><p><span style='background-color: initial;'>The blazing of a fiercy ball pierced through the dark skies,</span></p><p>Glowing with the rainy drops, to reflect the colorful sky.</p><p>The shyness of the rainbow is in the love with sky, coming out with the colors just to make the people in love with the sky.</p><p>Colors of Rainbow make both of them not to cry, the teary eyes though fell in love with the colorful sky.</p>'''


