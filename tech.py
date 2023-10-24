from newspaper import Article
from bs4 import BeautifulSoup
import requests
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime 
import os
import ipinfo
import socket
import json
from summarise import Summariser
cred = credentials.Certificate('./serviceKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
def check(url):
    with open('dup.txt', 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if url in line:
                return 1
    return 0
def Technology():
	url = "https://gadgets.ndtv.com/rss/feeds"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	news_items = []

	List2 = []
	for item in items:
		link = item.link.text
		
		news_items.append(link)
	news_items=news_items[1:15]

	'''page2 = requests.get('https://www.gadgetsnow.com/tech-news')
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='tech_list ctn_stories')
	itemst1=headl1.find_all(class_='w_tle')
	links=headl1.find_all('a',href=True)
	cc1=[link.get('href') for link in links]
	flag=0
	for i in cc1:
		flag=i.find("https://www.gadgetsnow.com")
		if flag == -1:
			i="https://www.gadgetsnow.com"+i
		if i not in List2:
			List2.append(i)
	List2=List2[1:14]'''

	for i in news_items:
		if i not in List2:
			List2.append(i)
	for i in List2:
		print(i)
	news_items = []
	i=1
	for item in List2:
		

			i=i+1
			p=check(item)
			print(p)
			if p != 1 :
				news_items.append(item)
	k=0
	for x in List2:
		
		article=Article(x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		t1=article.title
		print(t1)
		txt=article.text
		
		str2 = txt.replace("\n", "")
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		os.system('python classifier.py')
		f1 = open('category.txt','r')

		category=f1.read()
		if(category=='NA'):
			category='Technology'
		print(summ)
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.datetime.now(),
			    u'URL':x,
			    u'Category': category,
			    u'source':u'gadgetsnow'
		})
Technology()