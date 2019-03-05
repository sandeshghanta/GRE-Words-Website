import os
import re
import requests
import datetime
import feedparser
from nltk import tokenize,word_tokenize
from bs4 import BeautifulSoup
from global_functions import get_global_data,update_global_data,get_wordlist,is_relevant_sentence,add_reference,remove_file,is_text

def get_sentences(text):
	return tokenize.sent_tokenize(text)

def get_words_from_sentence(sentence):
	return word_tokenize(sentence)

def scrape_text_from_webiste(soup):
	data = []
	divs = soup.find_all("div",class_="Normal")
	for div in divs:
		sentences = div.find_all(text=True)
		for sentence in sentences:
			sentence = sentence.replace('\t','')
			sentence = sentence.replace('\n','')
			sentence = sentence.lstrip(" ")
			sentence = sentence.rstrip(" ")
			if (is_text(sentence)):
				data.append(sentence)
	text = " ".join(data)
	return text

def is_url(text):
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	result = re.match(regex,text)
	if (result):
		return True
	return False

def traverse_feed(feed,links):
	if (type(feed) is str):
		if (is_url(feed) and is_valid_link(feed)):
			links.append(feed)
	elif (type(feed) is feedparser.FeedParserDict):
		for key in feed:
			traverse_feed(feed[key],links)
	elif (type(feed) is list):
		for item in feed:
			traverse_feed(item,links)

def get_rss_feeds():
	url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
	feed = feedparser.parse(url)
	links = []
	traverse_feed(feed,links)
	links = list(set(links))
	return links

def is_valid_link(link):
	#There is no use of links pointing to root of webiste. So discarding such links 
	link = link.replace("http://","")
	link = link.replace("https://","")
	link = link.rstrip("/")
	if (link.count('/') > 1):
		return True
	return False

def scrape_webiste(link):
	soup = BeautifulSoup(r.text,"lxml")
	text = scrape_text_from_webiste(soup.body)
	return text

def index_relevant_words(sentences,file_path):
	#returns True if relevant words are found, else returns False 
	flag = False
	for sentence_index,sentence in enumerate(sentences):
		words = get_words_from_sentence(sentence)
		for word in words:
			if (word in wordlist and is_relevant_sentence(sentence,word)):
				add_reference(word,file_path+"::{}".format(sentence_index))
				print (word,sentence)
				flag = True
	return flag

if __name__ == "__main__":
	now = datetime.datetime.now()
	global_data = get_global_data()
	wordlist = get_wordlist(json_format=True)
	links = get_rss_feeds()
	for link in links:
		print (link)
		r = requests.get(link)
		text = scrape_webiste(link)
		if (not is_text(text)):
			continue
		sentences = get_sentences(text)
		file_name = "{}-{}-{}::{}".format(now.day,now.month,now.year,global_data['articles']['count'])
		global_data['articles']['count'] = global_data['articles']['count'] + 1
		file_path = os.path.join(global_data['articles']['storage_path'],file_name)
		with open(file_path,'w+') as file:
			file.write(text)
		words_indexed = index_relevant_words(text,file_path)
		if (not words_indexed):
			global_data['articles']['count'] = global_data['articles']['count'] - 1
			remove_file(file_path)
	result = update_global_data(global_data)
	if (not result):
		print ("ERROR! unable to update global_data.json file, the newly scraped articles might be overriden")	#LOG have to write these Errors to log file later