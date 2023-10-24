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
def predt(txt,category):
	#print(keyw)
	counter=0
	Covid=['cases','positive','covid19','coronavirus','recovery','tested','negative','covid','number','pandemic','testing','Covid-19','patients']
	Crime=['crime','murder','rape','tortured','death','serious','drugs','bail','victim','accused','trial','court','riots','case','cases','injured','jail','prison','alcoholic','abused','threat','police','station','illegal activities','illegal','arrested','threatened','booked','assault','assaulted','seized','Police']
	Politics=['govt','government','state','centre','shiv','sena','redevelopment','scheme','spent','report','villages','chief','appointed','sabha','policy','policies','plan','effective']
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
		category="Local"
		return category
def check(url):
    with open('dup.txt', 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if url in line:
                return 1
    return 0
    #DIGVIJAY
def Indianexpress(city):
	url = "https://indianexpress.com/section/cities/"+city+"/feed/"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")
#Duplicate URL is present or not 
	items = soup.findAll('item')
	news_items=[]
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
	for x in news_items:
		
		article=Article(x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		t1=article.title
		print(t1)
		txt=article.text
		txt=txt.replace("(Representational Image)","")
		txt=txt.replace("(File)","")
		txt=txt.replace("\n","")
		txt=txt.replace("(Representational)","")
		txt=txt.replace("The Indian Express is now on Telegram. Click here to join our channel (@indianexpress) and stay updated with the latest headlines","")
		txt=txt.replace("For all the latest "+city+" News, download Indian Express App.","")
		txt=txt.replace("For Corona Live Updates","")
		f = open("RL.txt", "w")
		f.write(txt)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		#read the summary file
		summ=f.read()
		#print(summ)
		f.close()
		os.system('python classifier.py')
		f1= open("category.txt","r")
		category=f1.read()
		pc=category
		if(category=='NA'):
			category=predt(txt,category)
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x,
			    u'City':city.capitalize(),
			    u'Category':category.capitalize(),
				u'source':u'Indian Express'	,	
		})		
#DIGVIJAY
Ilist=['delhi','kolkata','ahmedabad','mumbai','bangalore','chennai']
'''for i in Ilist:
	
	Indianexpress(i)	'''
Indianexpress('chennai')	
