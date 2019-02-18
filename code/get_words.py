import os
import json
import requests
from bs4 import BeautifulSoup
from global_functions import get_global_data

def scrape_words_and_write_to_file():
	url = "https://www.vocabulary.com/lists/128536"
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	tags = soup.find_all('a',attrs={'class': 'word dynamictext'})
	wordlist = []
	for tag in tags:
		wordlist.append(tag.contents[0])
	with open(global_data['wordlist_file_path'],"w+") as file:
		file.write(",".join(wordlist))

def read_words_from_file():
	#This function reads words from the global_words file
	with open(global_data['wordlist_file_path'],"r") as file:
		words = file.readline().split(',')
	return words

def clean_words(words):
	#This function makes all words to lower_case and removes duplicates
	for i in range(0,len(words)):
		words[i] = words[i].lower()
	words = list(set(words)) 	#to remove duplicates from the list
	return words

def split_words_to_files(words):
	word_list = [{} for i in range(0,26)]
	for word in words:
		word_list[ord(word[0])-97][word] = []

	char = 'a'
	for lis in word_list:
		with open("{}/{}_words.json".format(global_data['json_folder_path'],char),"w+") as file:
			json.dump(lis,file,indent=4)
		char = chr(ord(char)+1)

if __name__ == "__main__":
	global_data = get_global_data()
	print ("Scraping words") #TRACK
	scrape_words_and_write_to_file()
	words = read_words_from_file()
	words = clean_words(words)
	split_words_to_files(words)