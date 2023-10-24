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
def Indianexpress(city):
	url = "https://indianexpress.com/section/cities/"+city+"/feed/"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')
	news_items_sub=[]
	news_items_sub.clear()
	news_items = []
	previous_items = []
	for item in items:
	    link = item.link.text
	    news_items.append(link)
	news_items_sub=news_items[1:10]
	for i in previous_items:
		if i not in news_items_sub:
			news_items_sub.append(i)
	previous_items=news_items 
	for x in news_items_sub:
		
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
		#print(summ)
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
			    u'City':city
		})
		

def HindustanTimes(city):
	city1=city
	j=['14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
	
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
	Linkk=[]
	for i in cc1:
		if i not in Linkk:
			#print(i)
			Linkk.append(i)

	k=0
	Linkk=Linkk[1:13]


	k=1
	for x in Linkk:
		
		article=Article(x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		t1=article.title
		txt=article.text
		
		print(t1)
		f = open("s.txt", "w")
		f.write(txt)
		f.close()
		str2=remove_newlines('s.txt')
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		#print(summ)	
		img=article.top_image
		date1=article.publish_date
			
		doc_ref = db.collection(city1).document(city1+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x
		})
		k=k+1


def NewIndian(city):
	j=['29','30','31','32','33','34','35','36','37','38','39','40','41','42','43']
	page2 = requests.get('https://indianexpress.com/section/cities/'+city)
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='cities-stories')
	itemst1=headl1.find_all(class_='photo')
	links=headl1.find_all('a',href=True)
	cc1=[link.get('href') for link in links]
	Linkk=[]
	for i in cc1:
		if i not in Linkk:
			#print(i)
			Linkk.append(i)

	k=0
	Linkk=Linkk[1:13]
	for x in Linkk:
		
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
		str2=remove_newlines('s.txt')
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(city).document(city+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x
		})
		k=k+1
	
def RegionalNews(city):
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14','15','16','17','18','19','20']
	page2 = requests.get('https://timesofindia.indiatimes.com/city/'+city)
	soup = BeautifulSoup(page2.content,'html.parser')
	headl1=soup.find(class_='list5 clearfix')
	itemst1=headl1.find_all(class_='w_tle')
	links=headl1.find_all('a',href=True)
	cc=[link.get('href') for link in links]
	tt1=[item1.get_text() for item1 in itemst1 ]
	
	Linkk=[]
	for i in cc1:
		if i not in Linkk:
			#print(i)
			Linkk.append(i)

	k=0
	Linkk=Linkk[1:13]
	for x in Linkk:
		article=Article('https://timesofindia.indiatimes.com'+x)
		article.download()
		article.parse()
		article.nlp()
		key=article.keywords
		
		t1=article.title
		print(t1)
		img=article.top_image
		date1=article.publish_date
		text1=article.text
		#(text1)
		doc_ref = db.collection().document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x

		})
		k=k+1
def Technology():
	j=['1','2','3','4','5','6','7','8','9','10','11','15','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
	page1= requests.get('https://gadgets.ndtv.com/')
	soup = BeautifulSoup(page1.content,'html.parser')
	headl1=soup.find(class_='nlist bigimglist')
	itemst1=headl1.findAll(class_='caption')
	links=headl1.findAll('a',href=True)
	cc=[link.get('href') for link in links]
	List1=[]
	List2=[]
	for i in cc:
		if i not in List1:
			#print(i)
			List1.append(i)
	List1=List1[1:15]
	page2 = requests.get('https://www.gadgetsnow.com/tech-news')
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
	List2=List2[1:14]

	for i in List1:
		if i not in List2:
			List2.append(i)
	for i in List2:
		print(i)
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
		
		f = open("s.txt", "w")
		f.write(txt)
		f.close()
		str2=remove_newlines('s.txt')
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'Tech').document(u'tech'+j[k])
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x
		})
		


Nlist=['delhi','Kolkata','pune','mumbai','chennai','bangalore']
Hlist=['bengaluru','delhi','kolkata','pune','mumbai']
Ilist=['delhi','kolkata','pune','mumbai','bangalore','chennai']

