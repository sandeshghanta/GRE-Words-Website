import os
import json
import random
from nltk import tokenize

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

def get_wordlist():
	with open(global_data['wordlist_file_path'],'r') as wordlist_file:
		wordlist = wordlist_file.read().split(',')
	return wordlist

def get_list_of_json_objs():
	data = [{} for i in range(0,26)]
	for json_file_name in os.listdir(global_data['json_folder_path']):
		json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
		with open(json_file_path,'r') as json_file:
			data[ord(json_file_name[0])-97] = json.load(json_file)
	return data

def get_sentences(text):
	return tokenize.sent_tokenize(text)

if __name__ == "__main__":
	global_data = get_global_data()
	wordlist = get_wordlist()
	json_obj_list = get_list_of_json_objs()
	for book_name in os.listdir(global_data['books_folder_path']):
		print (book_name)
		with open(os.path.join(global_data['books_folder_path'],book_name),"r") as book:
			text = book.read()
			sentences = get_sentences(text)
			for sentence in sentences:
				print (sentence)
				words = sentence.split(" ")
				for word in words:
					word = word.lower()
					word = word.replace("\n","")
					if (word in wordlist):
						if (len(json_obj_list[ord(word[0])-97][word]) == 0):
							json_obj_list[ord(word[0])-97][word].append(1)
						else:
							json_obj_list[ord(word[0])-97][word][0] = json_obj_list[ord(word[0])-97][word][0] + 1
	
	# print (json_obj_list)
	# for char,json_obj in json_obj_list.items():
	# 	json_file_name = chr(97+char) + "_words.json"
	# 	json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
	# 	with open(json_file_path,'w+') as json_file:
	# 		json.dump(json_obj,json_file)