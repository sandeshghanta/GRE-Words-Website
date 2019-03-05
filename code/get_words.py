import os
import json
import requests
from bs4 import BeautifulSoup
from global_functions import get_global_data

def scrape_words():
	url = "https://www.vocabulary.com/lists/128536"
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	tags = soup.find_all('a',attrs={'class': 'word dynamictext'})
	wordlist = []
	for tag in tags:
		wordlist.append(tag.contents[0])
	wordlist = clean_wordlist(wordlist)
	return wordlist

def write_words_to_file(wordlist):
	with open(global_data['wordlist_file_path'],"w+") as file:
		file.write("::".join(wordlist))

def clean_wordlist(wordlist):
	#This function makes all words to lower_case and removes duplicates
	for i in range(0,len(wordlist)):
		wordlist[i] = wordlist[i].lower()
	wordlist = list(set(wordlist)) 	#to remove duplicates from the list
	return wordlist

if __name__ == "__main__":
	global_data = get_global_data()
	print ("Scraping words") #TRACK
	wordlist = scrape_words()
	write_words_to_file(wordlist)