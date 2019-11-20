'''
This script checks whether a post is a business post or not
usage:
just call busi_group(pass the user post description here) ans it will print whther a post is a business post or not
'''
from nltk.stem import SnowballStemmer
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def converter(string_post):
    '''
    This function removes html tags from inside the description and returns a clean string for our model to perform further operations.
    '''
    string_post=re.sub(r'http\S+', '', string_post, flags=re.MULTILINE)
    #print(string_post)
    string_post=string_post.replace('<.*?>|</.*?>', "")
    #string_post=(BeautifulSoup(string_post, 'lxml').text).replace('\xa0','')
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    #print(string_post)
    string_post.replace('\xa0','')
    string_post=tokenizer.tokenize(string_post)
    lmtzr = WordNetLemmatizer()
    stemmer = SnowballStemmer(language='english')
    for i in range(len(string_post)):
        string_post[i]=lmtzr.lemmatize(string_post[i].lower())
    string_post=" ".join(string_post)
    return string_post
def busi_group(user_post):
    '''
    This is the main function, it prints whether a post is business post or not.
    We are using CountVectorizer and MultinomialNB to predict whether a post is business post or not
    '''
    posts=pd.read_json('groups.json')#loading business posts
    for i in range(len(posts)):
        posts.description[i]=re.sub(r'http\S+', '', posts.description[i], flags=re.MULTILINE)
        posts.description[i]=(BeautifulSoup(posts.description[i], 'lxml').text).replace('\xa0','')
    posts['label']=1
    posts2=pd.read_json('groups2.json')#loading non business posts
    posts2.drop('id',inplace=True,axis=1)
    posts2['label']=0
    for i in range(len(posts2)):
        posts2.description[i]=re.sub(r'http\S+', '', posts2.description[i], flags=re.MULTILINE)
        posts2.description[i]=(BeautifulSoup(posts2.description[i], 'lxml').text).replace('\xa0','')
    final_data=posts.append(posts2)
    final_data.reset_index(drop=True, inplace=True)
    final_data=final_data.reindex(np.random.permutation(final_data.index))
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    for i in range(len(final_data)):
        #final_data.title[i]=tokenizer.tokenize(final_data.title[i])
        final_data.description[i]=tokenizer.tokenize(final_data.description[i])
    final_data.drop(['title'],axis=1,inplace=True)
    lmtzr = WordNetLemmatizer()
    #print(final_data.shape)
    for i in range(len(final_data)):
        #for j in range(len(final_data.title[i])):
            #final_data.title[i][j]=lmtzr.lemmatize(final_data.title[i][j].lower())
        for j in range(len(final_data.description[i])):
            final_data.description[i][j]=lmtzr.lemmatize(final_data.description[i][j].lower())
        #final_data.description[i]=lmtzr.lemmatize(final_data.description[i])
    for i in range(len(final_data)):
    #  final_data.title[i]=" ".join(final_data.title[i])
        final_data.description[i]=" ".join(final_data.description[i])
        #final_data.description[i]=lmtzr.lemmatize(final_data.description[i])
    vectorizer1 = CountVectorizer(stop_words='english')
    vectorizer2 = TfidfVectorizer(stop_words='english')
    fv1 = vectorizer1.fit_transform(final_data.iloc[:,0])
    fv2 = vectorizer2.fit_transform(final_data.iloc[:,0])
    #print(fv1.shape)
    loaded_model1 = pickle.load(open('count_vect2.sav', 'rb'))
    loaded_model2 = pickle.load(open('tf_idf2.sav', 'rb'))
    testt=user_post
    test_data=final_data.append({'description': converter(testt)}, ignore_index=True)
    fv3=vectorizer1.transform(test_data.iloc[:,0])
    fv4=vectorizer2.transform(test_data.iloc[:,0])
    a,b=fv3.shape
    c,d=fv4.shape
    #print(fv3.shape)
    #print(fv1.shape)
    if loaded_model1.predict(fv3[a-1])==[0]:
        print('Not a business post')
    else:
        print('business post')
busi_group('invest in media')