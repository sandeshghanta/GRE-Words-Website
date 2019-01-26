import os
import json
import random
from nltk import tokenize

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

def get_sentences(text):
	return tokenize.sent_tokenize(text)

if __name__ == "__main__":
	global_data = get_global_data()
	for book_name in os.listdir(global_data['books_folder_path']):
		print (book_name)
		with open(os.path.join(global_data['books_folder_path'],book_name),"r") as book:
			text = book.read()
			sentences = get_sentences(text)
			with open(os.path.join(global_data['sentences_folder_path'],book_name),"w+") as file:
				for sentence in sentences:
					if (sentence == "" or sentence == "\n" or len(sentence) == 0):
						continue
					sentence = sentence.replace("\n","")
					file.write(sentence+"\n")