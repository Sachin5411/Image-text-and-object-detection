'''
This Scripts find outs if there any abuse in the Text with the help of Keyword analysis

'''


from flashtext.keyword import KeywordProcessor
from nltk import tokenize
from nltk.corpus import stopwords
import numpy as np

def remove_stopwords(text,sw):
	'''
	This function removes stopwords from the text
		Parameters:
			Text, list of sw
		return:
			Clean Text
	'''
	x=str(text)
	x=x.split(' ')
	words=[w for w in x]
	sws=set(sw)
	useful_words=[w for w in words if w not in sws]
	cleaned=' '.join(useful_words)
	return cleaned

def find_abuse(description,kp0):
	'''
	This Function finds abuse in the text 
	Parameter:
		Description, Object of KeywordProcessor (added all the abusive words)
	'''
	x=str(description)
	y0 = kp0.extract_keywords(x)
	if len(y0)==0:
		print('Not Abusive')
		print('-'*50)
	else:
		print("Abusive ")
		print("Abusive words found " ,y0)
		print('-'*50)



def abusive_analysis(description):
	'''
	This function does all the prearrangement for keyword analysis and use find_abuse and remove_stopwords as a helper funcitons
	Parameter:
		description

	'''
	#opening the text file of abusive words
	with open('bad_words_list.txt','r') as f:
		c=f.readlines()
	s=c[0].split(',')

	abusive_words=[]
	for i in s:
		i=i[1:]
		abusive_words.append(i)

	keywords=np.array(abusive_words)
	kp0=KeywordProcessor() #creating object of KeywordProcessor

	for word in keywords:
		kp0.add_keyword(word) 
	sw=stopwords.words('english')
	to_remove=['[]','','1','()','||','=','.',',','\n',':',';','\\','//','/'] #some additional stopwords provided manually

	for i in to_remove:
		sw.append(i)
		clean=remove_stopwords(description,sw)

	find_abuse(clean,kp0)



