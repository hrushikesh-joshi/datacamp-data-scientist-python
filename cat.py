import nltk
import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
#word_tokenize accepts a string as an input, not a file. 
stop_words = set(stopwords.words('english')) 
file1 = open("RL.txt") 
line = file1.read()# Use this to read file content as a stream: 
words = line.split() 
for r in words: 
    if not r in stop_words: 
        appendFile = open('filteredtext.txt','w') 
        appendFile.write(" "+r) 
        appendFile.close() 
with open ("RL.txt", "r") as myfile:
    data=myfile.read().replace('\n', ' ')

data = data.split(' ')
fdist1 = nltk.FreqDist(data)
#print (fdist1.most_common(50))
for i in fdist1:
	print(i)