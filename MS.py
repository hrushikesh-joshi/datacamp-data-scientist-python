#SUMMARY
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words




from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from twitterscraper import query_tweets
import datetime as dt
import os
from newspaper import Article




#TIMES OF INDIA MUMBAI
page2 = requests.get('https://timesofindia.indiatimes.com/city/mumbai')
soup = BeautifulSoup(page2.content,'html.parser')
headl1=soup.find(class_='list5 clearfix')
itemst1=headl1.find_all(class_='w_tle')
links=headl1.find_all('a',href=True)
cc=[link.get('href') for link in links]
tt1=[item1.get_text() for item1 in itemst1 ]

#NDTV NEWS NASHIK

'''page3 = requests.get('https://www.dnaindia.com/topic/nashik')
soup1 = BeautifulSoup(page2.content,'html.parser')
headl2=soup1.find(class_='mrebolynwsrgtbx')
itemst2=headl2.find_all(class_='option-list')
links1=headl2.find_all('a',href=True)
cc1=[link.get('href') for link in links1]
tt2=[item1.get_text() for item1 in itemst2 ]
print(tt2)'''
keys=[]
summ=[]
LANGUAGE = "english"
SENTENCES_COUNT = 5
sum1=""
sen=""
Summary=[]
text1=""

summary=[]
sen=""
sen1=""
LANGUAGE = "english"
SENTENCES_COUNT = 3




try:
	for x in cc:
		article=Article('https://timesofindia.indiatimes.com'+x)
		article.download()
		article.parse()
		article.nlp()
		keys.append(article.keywords)
		text1=article.text
		
		f = open("content.txt", "w") 
		f.write(text1) 
		f.close() 

	#url = 'https://timesofindia.indiatimes.com'+x


	#parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	# or for plain text files
		parser = PlaintextParser.from_file("content.txt", Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)

		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words(LANGUAGE)

		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			sen=str(sentence)
			sen1=sen1+sen
		summary.append(sen1)
		sen1=""
	#print(keys)

except Exception as x:
    print(x)





print(summary)
#print(tt1)
#for i in tt1: 
   #tt.append(i) 
#print(tt1)
Mumbaiheadlines = pd.DataFrame (
{'headline': tt1,
	'URL':cc,
	'Keywords':keys,
	'summary':summary
	

	
})
print(Mumbaiheadlines)
Mumbaiheadlines.to_csv('Mumbaiheadlines.csv')
##