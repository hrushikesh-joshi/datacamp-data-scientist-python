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

def Sports():
	url = "https://www.tribuneindia.com/rss/feed?catId=50"

	resp = requests.get(url)

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

	print()
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
		os.system('python classifier.py')
		f1 = open('category.txt','r')

		category=f1.read()
		
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
			    u'Category':category.capitalize()
		})
Sports()
