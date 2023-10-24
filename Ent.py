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
def Entertainment():
	url = "https://indianexpress.com/section/entertainment/feed/"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')
	print(items)
	news_items = []

	for item in items:
		link = item.link.text
		news_items.append(link)

	news_items=news_items[1:10]
	
	url = "https://www.hindustantimes.com/rss/world-cinema/rssfeed.xml"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	worldcinema_items = []

	for item in items:
		link = item.link.text
		worldcinema_items.append(link)
	worldcinema_items=worldcinema_items[1:10]
	for i in news_items:
		if i not in worldcinema_items:
			worldcinema_items.append(i)

	url = "https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	news_items = []
	hollywood =[]
	k=1
	for item in items:
		link = item.link.text
		hollywood.append(link)
	hollywood=hollywood[1:10]
	for i in worldcinema_items:
		if i not in hollywood:
			hollywood.append(i)
	for item in hollywood:
		if k !=20:
			
			k=k+1
			p=check(item)
			print(p)
			if p != 1 :
				news_items.append(item)
	f=open("dup.txt","a")
	for i in news_items:
		f.write(i)
		f.write('\n')
	f.close()
	for x in news_items:
		
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
		os.system('python smm.py')
		f = open("ss.txt", "r")
		summ=f.read()
		f.close()
		summ = summ.replace("Click here to join our channel (@indianexpress) and stay updated with the latest headlinesFor all the latest","")
		os.system('python classifier.py')
		f1 = open('category.txt','r')

		category=f1.read()
		if(category=='NA'):
			category='Entertainment'
		print(summ)
		img=article.top_image
		date1=article.publish_date
		if(x.find("indianexpress.com")!=-1):
			source="Indian Express"
		else:
			source="Times of India"
		print(source)
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.datetime.now(),
			    u'URL':x,
			    u'Category':category,
			    u'source':source,
		})	 
Entertainment()