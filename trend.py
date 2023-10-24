from newspaper import Article
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt
import os
import ipinfo
import socket
import json
import requests
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
def predt(txt,category):
	#print(keyw)
	counter=0
	Covid=['cases','positive','covid19','coronavirus','recovery','tested','negative','covid','number','pandemic','testing','Covid-19','patients']
	Crime=['crime','murder','rape','tortured','death','serious','drugs','bail','victim','accused','trial','court','riots','case','injured','jail','prison','alcoholic','abused','threat','police','station','illegal activities','illegal','arrested','threatened','booked','assault','assaulted','seized','Police']
	Politics=['govt','government','state','centre','shiv','sena','redevelopment','scheme','spent','report','villages','chief','appointed','sabha','policy','policies','plan','effective','ministers']
	Health=[]
	Business=[]
	counter=0;
	for i in Covid:
		if (txt.find(i)!=-1):
			counter=counter+1
	if(counter>=2):
		print("COVID")
		return "Covid19"
	
	counter=0;
	for i in Politics:
		if(txt.find(i)!=-1):
			counter=counter+1
	if(counter>=2):
		print("Politics")
		return "Politics"
		
	counter1=0;
	for i in Crime:
		#print(i)
		if(txt.find(i)!=-1):
			counter1=counter1+1
			print(counter1)
	if(counter1>=2):
		print("Crime")
		return "Crime"
	else :
		print("NOT")
		f1 = open("cat1.txt","r")
		category= f1.read()
		f1.close()
		print(category)
		return category

from bs4 import BeautifulSoup
def Trending():
	url1 = "https://www.hindustantimes.com/rss/topnews/rssfeed.xml"

	resp = requests.get(url1)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	news_items = []

	for item in items:
		link = item.link.text
		p=check(link)
		print(p)
		if p != 1 :
			news_items.append(link)
	f=open("dup.txt","a")
	for i in news_items:
		f.write(i)
		f.write('\n')
	f.close()
		
	for i in news_items:
		
		article=Article(i)
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

		Category=f1.read()
		if(Category=='NA'):
			Category=predt(txt,category)
		#print(Category)
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'Trending').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.now(),
			    u'URL':i,
			    u'Category':Category,
			    u'source':u'Hindustan Times'
		})
def Trending1():
	url1 = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

	resp = requests.get(url1)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	news_items = []

	for item in items:
		link = item.link.text

		p=check(link)
		print(p)
		if p != 1 :
			news_items.append(link)
	f=open("dup.txt","a")
	for i in news_items:
		f.write(i)
		f.write('\n')
	f.close()
	for i in news_items:
		
		article=Article(i)
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

		Category=f1.read()
		if(Category=='NA'):
			Category=predt(txt,Category)
		#print(Category)
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'Trending').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.now(),
			    u'URL':i,
			    u'Category':Category,
			    u'source':u'Times of India'
		})
def Trending2():
	url1 = "https://feeds.feedburner.com/ndtvnews-top-stories"

	resp = requests.get(url1)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	news_items = []

	for item in items:
		link = item.link.text

		p=check(link)
		print(p)
		if p != 1 :
			news_items.append(link)
	f=open("dup.txt","a")
	for i in news_items:
		f.write(i)
		f.write('\n')
	f.close()
	for i in news_items:
		
		article=Article(i)
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

		Category=f1.read()
		if(Category=='NA'):
			Category=predt(txt,Category)
		print(Category)
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'Trending').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.now(),
			    u'URL':i,
			    u'Category':Category,
			    u'source':u'NDTV'
		})
def Trending3():
	url1 = "https://www.news18.com/rss/buzz.xml"

	resp = requests.get(url1)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	news_items = []
	i=1
	for item in items:
		if i !=20:
			link = item.link.text
			i=i+1
			p=check(link)
			print(p)
			if p != 1 :
				news_items.append(link)
	f=open("dup.txt","a")
	for i in news_items:
		f.write(i)
		f.write('\n')
	f.close()
	for i in news_items:
		
		article=Article(i)
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

		Category=f1.read()
		print(Category)
		if(Category=='NA'):
			Category=predt(txt,Category)
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'Trending').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.now(),
			    u'URL':i,
			    u'Category':Category
			    
		})

Trending1()
#Trending2()

#Trending()
#Trending3()
from datetime import date

today = date.today()