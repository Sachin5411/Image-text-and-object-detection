'''
this script print whether a post is spam or not
usage-
just pass the description in spam_group and it will print whether that was a spam post or not
'''
from nltk.stem import SnowballStemmer;
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
    #string_post=(BeautifulSoup(string_post, "lxml").text).replace('\xa0','')
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
def spam_group(user_post):
    '''
    This is the main function, it prints whether a post is spam post or not.
    We are using CountVectorizer and MultinomialNB to predict whether a post is spam post or not
    '''
    user_data=pd.read_csv('spam.csv',encoding='latin-1')
    user_data = user_data[['v1','v2']]
    user_data = user_data.rename(columns={'v1':'label','v2':'text'})
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    user_data.text=user_data.text.map(lambda d : tokenizer.tokenize(d))
    stemmer = SnowballStemmer(language='english')
    user_data.text = user_data.text.map(lambda sen : [stemmer.stem(word) for word in sen])
    user_data.text = user_data.text.map(lambda sen : ' '.join(sen))
    vectorizer1 = CountVectorizer(stop_words='english')
    vectorizer2 = TfidfVectorizer(stop_words='english')
    fv1 = vectorizer1.fit_transform(user_data.text)
    fv2 = vectorizer2.fit_transform(user_data.text)
    #label = user_data.label.map(lambda elem : 1 if elem.strip()=='spam' else 0 )
    loaded_model1 = pickle.load(open('count_vect_spam.sav', 'rb'))
    loaded_model2 = pickle.load(open('tf_idf_spam.sav', 'rb'))
    testt=user_post
    #test_data=user_data.text
    test_data=user_data.append({'text':converter(testt)}, ignore_index=True)
    fv3=vectorizer1.transform(test_data.text)
    fv4=vectorizer2.transform(test_data.text)
    a,b=fv3.shape
    c,d=fv4.shape
    if loaded_model1.predict(fv3[a-1])==[0]:
        print('not_spam')
    else:
        print('spam')
    #print(test_data.tail(5))
# spam_group('hi need to talk about some stuff. lets meet around 5. samar also coming')