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
city="Pune"
a='https://indianexpress.com/article/cities/chennai/tamil-nadu-full-list-of-red-orange-and-green-zones-6389241/'

article=Article(a)
article.download()
article.parse()
article.nlp()
key=article.keywords
t1=article.title
txt=article.text
txt=txt.replace("(Representational Image)","")
txt=txt.replace("(File)","")
txt=txt.replace("\n","")
txt=txt.replace("(Representational)","")
txt=txt.replace("The Indian Express is now on Telegram. Click here to join our channel (@indianexpress) and stay updated with the latest headlines","")
txt=txt.replace("For all the latest "+city+" News, download Indian Express App.","")
txt=txt.replace("For Corona Live Updates","")
print(txt)