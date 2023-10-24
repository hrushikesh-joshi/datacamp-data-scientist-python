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
	
def timesofindia(city):
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14','15','16','17','18','19','20']
	
	page2 = requests.get('https://timesofindia.indiatimes.com/city/'+city)
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='list5 clearfix')
	itemst1=headl1.find_all(class_='w_tle')
	links=headl1.find_all('a',href=True)
	cc=[link.get('href') for link in links]
	tt1=[item1.get_text() for item1 in itemst1 ]
	
	Linkk=[]
	for i in cc:
		if i not in Linkk:
			#print(i)
			Linkk.append('https://timesofindia.indiatimes.com'+i)

	k=0
	Linkk=Linkk[1:20]
	news_items=[]
	i=1
	for item in Linkk:
		if i !=20:
			
			i=i+1
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
		f = open("s.txt", "w")
		f.write(txt)
		f.close()
		str2 = txt.replace("\n", "")
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		
		os.system('python classifier.py')
		f1= open("category.txt","r")
		category=f1.read()
		pc=category
		if(category=='NA'):
			category=predt(txt,category)
		img=article.top_image
		date1=article.publish_date
		text1=article.text
		#(text1)
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.datetime.now(),
			    u'URL':x,
			    u'City':city.capitalize(),
			    u'Category':category.capitalize(),
			    u'source':u'Times Of India'

		})
		k=k+1
Tlist=['mumbai','delhi','bangalore','hyderabad','Kolkata','Chennai','agra','Ajmer','Amritsar','Aurangabad','Bhopal','Coimbatore','Chandigarh','Goa','Gurgaon','Guwahati','Imphal','Jaipur','Jammu','Lucknow','Kochi','Mysore','Nashik','puducherry']
#for i in Tlist:
	#timesofindia(i)
timesofindia('Amritsar')


