import os
import bs4
import time
import requests
import multiprocessing
from bs4 import BeautifulSoup
from nltk import tokenize,word_tokenize
from global_functions import remove_file,get_global_data,add_reference,is_relevant_sentence,get_wordlist,create_folder,is_text


def get_sentences(text):
	return tokenize.sent_tokenize(text)


def get_words_from_sentence(sentence):
	return word_tokenize(sentence)


def extract_text(item):
	if (isinstance(item,bs4.element.NavigableString)):
		return item
	if (len(list(item.children)) != 0):
		text = ""
		for child in item.children:
			if ("sup" != child.name):
				child_text = extract_text(child)
				if (child_text):
					text += child_text 
		return text


def scrape_webiste(link):
	r = requests.get(link)
	soup = BeautifulSoup(r.text,"lxml")
	text = ""
	paras = soup.find_all("p")
	for para in paras:
		para_text = extract_text(para)
		if (is_text(para_text)):
			text += para_text
	return text

# def index_relevant_words(text,file_path):
# 	#returns True if relevant words are found, else returns False 
# 	flag = False
#	sentences = get_sentences(text)
# 	for sentence_index,sentence in enumerate(sentences):
# 		words = get_words_from_sentence(sentence)
# 		for word in words:
# 			if (word in wordlist and is_relevant_sentence(sentence,word)):
# 				add_reference(word,file_path+"::{}".format(sentence_index))
# 				print (word,sentence)
# 				flag = True
# 	return flag


def check_words(text):
	#returns True if relevant words are found, else returns False
	sentences = get_sentences(text)
	for sentence_index,sentence in enumerate(sentences):
		words = get_words_from_sentence(sentence)
		for word in words:
			if (word in wordlist and is_relevant_sentence(sentence,word)):
				return True
	return False


def scrape(max_tries):
	useful_documents = 0
	scraped = 0
	for i in range(max_tries):
		link = get_random_link()
		text = scrape_webiste(link)
		print (link)
		file_name = link.rsplit('/',1)[-1] + ".txt"
		file_path = os.path.join(global_data['books_folder_path']['wikipedia'],file_name)
		with open(file_path,"w+") as file:
			file.write(text)
		words_found = check_words(text)
		if (not words_found):
			remove_file(file_path)
			useful_documents = useful_documents - 1
		useful_documents = useful_documents + 1
		scraped = scraped + 1
	return (useful_documents,scraped)


def get_random_link():
	r = requests.get("https://en.wikipedia.org/wiki/Special:Random")
	return r.url


if __name__ == "__main__":
	max_tries = int(input("Enter no of docs to be scraped "))
	start_time = time.time()
	global_data = get_global_data()
	wordlist = get_wordlist(json_format=True)
	# print (wordlist)
	create_folder(global_data['books_folder_path']['wikipedia'])
	useful_documents = 0
	scraped = 0
	links = [[] for i in range(global_data['cores_count'])]
	pool = multiprocessing.Pool(processes=global_data['cores_count'])
	args = [(max_tries//global_data['cores_count'],) for i in range(global_data['cores_count'])]
	results = pool.starmap(scrape,args)
	for result in results:
		useful_documents = useful_documents + result[0]
		scraped = scraped + result[1]
	print ("scraped {} and found {} useful documents".format(scraped,useful_documents))
	print ("took " + str(time.time()-start_time) + " seconds")
	
