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
def predt(txt,category):
	#print(keyw)
	counter=0
	Covid=['cases','positive','covid19','coronavirus','recovery','tested','negative','covid','number','pandemic','testing','Covid-19','patients']
	Crime=['crime','murder','rape','tortured','death','serious','drugs','bail','victim','accused','trial','court','riots','case','cases','injured','jail','prison','alcoholic','abused','threat','police','station','illegal activities','illegal','arrested','threatened','booked','assault','assaulted','seized','Police','cheated','fled','suspects','suspect','complaint']
	Politics=['govt','government','state','centre','shiv','sena','redevelopment','scheme','spent','report','villages','chief','appointed','sabha','policy','policies','plan','effective','elected','opposition','BJP','Congress','poll','election','leader']
	Health=[]
	Business=[]
	counter=0;
	for i in Covid:
		if (txt.find(i)!=-1):
			counter=counter+1
	if(counter>=3):
		print("COVID")
		return "Covid19"
	
	counter=0;
	for i in Politics:
		if(txt.find(i)!=-1):
			counter=counter+1
	if(counter>=3):
		print("Politics")
		return "Politics"
		
	counter1=0;
	for i in Crime:
		#print(i)
		if(txt.find(i)!=-1):
			counter1=counter1+1
			print(counter1)
	if(counter1>=3):
		print("Crime")
		return "Crime"
	else :
		print("LOCAL")
		category='Local'
		return category

def check(url):
    with open('dup.txt', 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if url in line:
                return 1
    return 0
def Indianexpress(city):
	url = "https://indianexpress.com/section/cities/"+city+"/feed/"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

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
		str2 = txt.replace("\n", "")
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		print(summ)
		f.close()
		if (x.find('covid') != -1) :
			category='COVID'
		else:
			
			os.system('python classifier.py')
			f1 = open('category.txt','r')

			category=f1.read()
			f1.close()
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'try').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x,
			    u'City':city.capitalize(),
			    u'Category':category.capitalize()
		})
		

def HindustanTimes(city):
	city1=city

	
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
		txt=article.text
		
		print(t1)
		
		str2 = txt.replace("\n", "")
		
		f = open("BS.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		print(summ)	
		img=article.top_image
		date1=article.publish_date
		if (x.find('covid') != -1) :
			category='COVID'
		else:
			
			os.system('python classifier.py')
			f1 = open('category.txt','r')

			category=f1.read()
			f1.close()

		category=f1.read()
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':date1,
			    u'URL':x,
			    u'City':city1.capitalize(),
			    u'Category':category.capitalize()
		})
		k=k+1


def NewIndian(city,id):
	
	
	url1 = 'https://www.newindianexpress.com/Cities/'+city+'/rssfeed/?id='+id+'&getXmlFeed=true'

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
		if (x.find('covid') != -1) :
			category='COVID'
		else:
			
			os.system('python classifier.py')
			f1 = open('category.txt','r')

			category=f1.read()
			f1.close()

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
			    u'City':city.capitalize(),
			    u'Category':category.capitalize()
		})
		
	
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
		f.close()
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
			    u'source':u'Times Of India',
		})
		k=k+1
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

	for i in news_items:
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
		str2 = txt.replace("\n", "")
		f = open("RL.txt", "w")
		f.write(str2)
		f.close()
		os.system('python summary.py')
		f = open("ss.txt", "r")
		summ=f.read()
		
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.now(),
			    u'URL':x,
			    u'Category':u'Technology'
		})
		
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
		os.system('python summary.py')
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


def Entertainment():
	url = "https://www.hindustantimes.com/rss/bollywood/rssfeed.xml"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

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

	url = "https://www.hindustantimes.com/rss/hollywood/rssfeed.xml"

	resp = requests.get(url)

	soup = BeautifulSoup(resp.content, features="xml")

	items = soup.findAll('item')

	hollywood = []

	for item in items:
		link = item.link.text
		hollywood.append(link)
	hollywood=hollywood[1:10]
	for i in worldcinema_items:
		if i not in hollywood:
			hollywood.append(i)
	for x in hollywood:
		
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
		
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.now(),
			    u'URL':x,
			    u'Category':u'Entertainment'
		})	  
def Markets():
	url1 = "https://www.moneycontrol.com/rss/business.xml"

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
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.datetime.now(),
			    u'URL':i,
			    u'Category':u'Business'
			    
		})
	M2()
def M2():
	url2 = "https://www.moneycontrol.com/rss/economy.xml"

	resp = requests.get(url2)

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
		
		img=article.top_image
		date1=article.publish_date
		doc_ref = db.collection(u'news').document()
		doc_ref.set({
				u'title': t1,
			    u'image': img,
			    u'keywords': key,
			    u'summary': summ,
			    u'Date':datetime.datetime.now(),
			    u'URL':i,
			    u'Category':u'Business'
			    
		})
 

Nlist=['delhi','Kolkata','pune','mumbai','chennai','bangalore','Ahmedabad','Kochi']
Hlist=['bengaluru','delhi','kolkata','pune','mumbai']
Ilist=['delhi','kolkata','ahmedabad','mumbai','bangalore','chennai']
Tlist=['mumbai','delhi','bangalore','hyderabad','Kolkata','Chennai','agra','Ajmer','Amritsar','Aurangabad','Bhopal','Coimbatore','Chandigarh','Goa','Gurgaon','Guwahati','Imphal','Jaipur','Jammu','Lucknow','Kochi','Mysore','Nashik','puducherry']

'''for i in Ilist:
	
	Indianexpress(i)
	for i in Hlist:
	HindustanTimes(i)
for i in Nlist:
	if i == 'delhi':
		NewIndian(i,'340')
	elif i == 'Kolkata':
		NewIndian(i,'342')
	elif i == 'mumbai':
		NewIndian(i,'341')
	elif i == 'bangalore':
		NewIndian('Bengaluru','342')
	elif i == 'chennai':
		NewIndian(i,'181')
	elif i == 'Ahmedabad':
		NewIndian(i,'343')
	elif i == 'Kochi':
		NewIndian(i,'185')

for i in Tlist:
	timesofindia(i)HindustanTimes('mumbai')'''

timesofindia('pune')


