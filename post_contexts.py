import database_connection
import bs4
import ast
#from darkflow.net.build import TFNet
import cv2
from bs4 import BeautifulSoup
from pymemcache.client import base
from bs4.element import Comment
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
'''
this script checks for the context of post or what group does a post belong to
usage:
just pass decription in context_analysis()
it will print all the groups that the post belongs to
'''
def tag_visible(element):
    '''This function is a helper function to removes all the html tags from the element
            it finds all visible text excluding scripts, comments, css etc.
            
            return:
                True or False
    '''
    #function to remove html tags
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    ''' This function is used to extract text from html page ,it uses function tag_visible() as a helper funciton 
            parameter:
                html content of page
            return:
                String of all visible text
    '''
    #function to extract text from html page
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
def context_analysis(post):
    client=base.Client(('localhost',11211))
    stop = stopwords.words('english')
    articles=[post]
    predefined_groups=client.get('0')#
    '''getting all the groups from cache
    provided all the groups are in cache.
    '''
    k=str(predefined_groups).replace("b\'",'').replace("\'","").replace("\'","") 
    res=ast.literal_eval(k)
    # print(articles[0])
    for i in articles:
        word_tokens_post = word_tokenize(text_from_html(i))
        for j in range(len(res)):
            w_token=word_tokenize(str(res[j]))
            filter_grp=[a for a in w_token if a not in stop]
            res[j]=' '.join(filter_grp)
        #print(res)
    #lmtzr = WordNetLemmatizer()
    #group_list=str()
        #print('yesss')
        filtered_sentence = [a for a in word_tokens_post if a not in stop]
        filtered_sentence=[x.lower() for x in filtered_sentence]
        filtered_sentence=' '.join(filtered_sentence)
        for j in range(len(res)):
            if res[j].lower() in filtered_sentence:
                print(str(res[j]))
               # print(filtered_sentence)
    #filtered_groups=[a for a in word_tokens if a not in stop]'''
'''
example given below->'''

#context_analysis('<p>The eyes of skies when filled up with the tears,</p><p>Dark clouds like eyelids cover its alluring blue color.</p><p>The Subtle winds swirls into usher in the showers of dismal,</p><p>Dropping out the thick teardrops that accompanied with thunder screams,<span style="background-color: initial;">Just with the celestial intervention.</span></p><p><span style="background-color: initial;"><img class="fr-dib fr-draggable" src="https://s3.ap-south-1.amazonaws.com/atg-test-s3/assets/Backend/img/group_img/cover/Accessories Inventors.jpg"></span><br></p><p>The breezy sky with the drop of the tear,</p><p><span style="background-color: initial;">The blazing of a fiercy ball pierced through the dark skies,</span></p><p>Glowing with the rainy drops, to reflect the colorful sky.</p><p>The shyness of the rainbow is in the love with sky, coming out with the colors just to make the people in love with the sky.</p><p>Colors of Rainbow make both of them not to cry, the teary eyes Content Marketing though fell in love with the colorful sky.</p>')