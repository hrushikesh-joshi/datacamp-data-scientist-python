from newspaper import Article
from bs4 import BeautifulSoup
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt
import os
import ipinfo
import socket
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from newspaper import Article

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
access_token = '767b0792edc479'
handler = ipinfo.getHandler(access_token)
ip_address = IPAddr
details = handler.getDetails()
lo=details.city
print(lo)
cred = credentials.Certificate('./serviceKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()




def _create_frequency_table(text_string) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.
    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words

        '''
        Notice that a potential issue with our score algorithm is that long sentences will have an advantage over short sentences. 
        To solve this, we're dividing every sentence score by the number of words in the sentence.
        
        Note that here sentence[:10] is the first 10 character of any sentence, this is to save memory while saving keys of
        the dictionary.
        '''

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def run_summarization(text):
	    # 1 Create the word frequency table
    freq_table = _create_frequency_table(text)

    '''
    We already have a sentence tokenizer, so we just need 
    to run the sent_tokenize() method to create the array of sentences.
    '''
    print(text)
    # 2 Tokenize the sentences
    sentences = sent_tokenize(text)

    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)

    return summary

def NDTV(city):
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14']
	page2 = requests.get('https://www.ndtv.com/'+city+'-news')
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='new_storylising')
	itemst1=headl1.find_all(class_='new_storylising_img')
	links=headl1.find_all('a',href=True)
	cc1=[link.get('href') for link in links]
	cc=cc1[1:15]


	k=1
	for x in cc:
		
		article=Article(x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		t1=article.title
		print(t1)
		txt=article.summary
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(city).document(city+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': txt,
			    u'Date':date1
		})
		k=k+1

def HindustanTimes(city):
	city1=city
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14']
	
	if city=='bengaluru' or city=='bangalore' :
		city1='bangalore'
	if city=='kolkata' or city=='bengaluru':

		page2 = requests.get('https://www.hindustantimes.com/'+city)
	else :
		page2= requests.get('https://www.hindustantimes.com/'+city+'-news')
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='latest-news-morenews more-latest-news more-separate newslist-sec')
	itemst1=headl1.find_all(class_='media-heading headingfour')
	links=headl1.find_all('a',href=True)
	cc1=[link.get('href') for link in links]
	cc=cc1[1:15]


	k=1
	for x in cc:
		
		article=Article(x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		t1=article.title
		txt=article.text
		#print(txt)
		summ=run_summarization(txt)	
		#print(summ)
		img=article.top_image
		date1=article.publish_date
			
		doc_ref = db.collection(city1).document(city1+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1
		})
		k=k+1
def Indianexpress(city):
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14']
	page2 = requests.get('https://indianexpress.com/section/cities/'+city)
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='cities-stories')
	itemst1=headl1.find_all(class_='photo')
	links=headl1.find_all('a',href=True)
	cc1=[link.get('href') for link in links]
	cc=cc1[1:15]


	k=1
	for x in cc:
		
		article=Article(x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		t1=article.title
		txt=article.text
		txt=txt.strip('\n')
		print(txt)
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(city).document(city+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': txt,
			    u'Date':date1
		})
		k=k+1
def RegionalNews(city):
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14','16','17','18','19','20']
	page2 = requests.get('https://timesofindia.indiatimes.com/city/'+city)
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='list5 clearfix')
	itemst1=headl1.find_all(class_='w_tle')
	links=headl1.find_all('a',href=True)
	cc=[link.get('href') for link in links]
	tt1=[item1.get_text() for item1 in itemst1 ]
	
	cc1=cc[1:20]
	k=1
	for x in cc1:
		article=Article('https://timesofindia.indiatimes.com'+x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		
		t1=article.title
		img=article.top_image
		date1=article.publish_date
		text1=article.text
		print(text1)
		doc_ref = db.collection(city).document(city+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': text1,
			    u'Date':date1
		})
		k=k+1




if __name__ == '__main__':
    
	Nlist=['delhi','Kolkata','pune','mumbai','chennai','bangalore']
	Hlist=['bengaluru','delhi','kolkata','pune','mumbai']
	Ilist=['delhi','kolkata','pune','mumbai','bangalore','chennai']

	#NDTV('delhi')
	Indianexpress('delhi')
	#RegionalNews('nashik')

#RegionalNews(lo)    	
'''for l in Nlist :
	NDTV(l)'''
'''for l in Hlist :
	HindustanTimes(l)
for l in Ilist :
	Indianexpress(l)
'''