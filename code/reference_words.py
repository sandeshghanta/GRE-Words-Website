import os
import re
import time
import json
import pickle
import random
from nltk import tokenize
import multiprocessing
from global_functions import get_global_data,get_wordlist,get_sys_args

def get_list_of_json_objs():
	data = [{} for i in range(0,26)]
	for json_file_name in os.listdir(global_data['json_folder_path']):
		if (json_file_name == "outfile"):	#Remove later, this is just for testing purpose
			continue
		json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
		with open(json_file_path,'r') as json_file:
			data[ord(json_file_name[0])-97] = json.load(json_file)
	return data

def reference_words(books_list,json_obj_list):
	for book in books_list:
		book_name = os.path.splitext(book['book_name'])[0]	#To remove the .txt extension, our folder will not contain that extension
		book_source = book['book_source']
		print ("Book: " + book_name)	#TRACK
		for chunk_name in os.listdir(os.path.join(global_data['chunks_folder_path'][book_source],book_name)):
			chunk_path = os.path.join(global_data['chunks_folder_path'][book_source],book_name,chunk_name)
			with open(chunk_path,'r') as chunk:
				chunk_data = chunk.read()
				sentences = chunk_data.split("::")
				for sentence_index,sentence in enumerate(sentences):
					words = re.split(', | |',sentence)
					for word in words:
						word = word.lower()
						word = word.replace("\n","")
						if (word in wordlist):
							json_obj_list[ord(word[0])-97][word].append(book_source+"::"+book_name+"::"+chunk_name+"::"+str(sentence_index))
	return json_obj_list

if __name__ == "__main__":
	start_time = time.time()
	global_data = get_global_data()
	args = get_sys_args()
	args_set = True
	if (len(args) == 0):
		args_set = False
	wordlist = get_wordlist(json_format=True)
	process_json_obj_list = [get_list_of_json_objs() for i in range(global_data['cores_count'])]
	json_obj_list = get_list_of_json_objs()
	books_list = [[] for i in range(global_data['cores_count'])]
	for book_source in global_data['books_folder_path']:
		if (args_set):
			if (book_source not in args):
				continue
		for index,book_name in enumerate(os.listdir(global_data['books_folder_path'][book_source])):
			books_list[index%global_data['cores_count']].append({"book_name":book_name,"book_source":book_source})
	pool = multiprocessing.Pool(processes=global_data['cores_count'])
	args = [(books_list[i],process_json_obj_list[i]) for i in range(global_data['cores_count'])]
	results = pool.starmap(reference_words,args)

	references = get_list_of_json_objs()
	for json_obj_list in results:
		for i in range(0,26):
			references[i] = {**references[i],**json_obj_list[i]}

	with open('json_data/outfile', 'wb') as file:
	    pickle.dump(references,file)

	# with open('json_data/outfile',"rb") as file:
	# 	references = pickle.load(file)
		
	for i in range(0,26):
		json_file_name = chr(97+i) + "_words.json"
		json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
		with open(json_file_path,'w+') as json_file:
			json.dump(references[i],json_file,indent=4)
	print ("took " + str(time.time()-start_time) + " seconds")