
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
article=Article('https://www.carandbike.com/news/tvs-motor-company-announces-salary-cuts-for-employees-2234905')
article.download()
article.parse()
article.nlp()
key=article.keywords
t1=article.title
txt=article.text
ss='s'
print(t1)
#print(txt)
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
if (ss.find('covid') != -1) :
	category='COVID'
else:
	
	os.system('python classifier.py')
	f1 = open('category.txt','r')

	category=f1.read()
	f1.close()