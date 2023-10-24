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
from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer as sumytoken
from sumy.summarizers.lex_rank import LexRankSummarizer





d
  
      	
show_article('https://www.hindustantimes.com/pune-news/all-shops-in-non-containment-zones-open-till-7pm-says-pune-police-chief/story-gJ9yNw27HXl5GAlwM5BwiI.html')