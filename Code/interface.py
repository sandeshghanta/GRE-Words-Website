import os
import json

def clean_word(word):
	word = word.lower()
	word = word.replace("\n","")
	return word

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

def get_list_of_json_objs():
	data = [{} for i in range(0,26)]
	for json_file_name in os.listdir(global_data['json_folder_path']):
		if (json_file_name == "outfile"):	#Remove later, this is just for testing purpose
			continue
		json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
		with open(json_file_path,'r') as json_file:
			data[ord(json_file_name[0])-97] = json.load(json_file)
	return data

def get_references(word):
	json_file_name  = word[0] + "_words.json"
	json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
	with open(json_file_path,"r") as json_file:
		json_data = json.load(json_file)
		if word in json_data:
			return json_data[word]
	return null

def get_sentences_from_refs(references,word):
	sentences = []
	for reference in references:
		book_name,chunk_name = reference.split("::")
		chunk_path = os.path.join(global_data['chunks_folder_path'],book_name,chunk_name)
		with open(chunk_path,'r') as chunk:
			sentences_in_chunk = chunk.read().split("::")
			for sentence in sentences_in_chunk:
				if word in sentence:
					sentences.append(sentence)
	return sentences

if __name__ == "__main__":
	global_data = get_global_data()
	json_obj_list = get_list_of_json_objs()
	while (True):
		word = str(input("Enter word "))
		word = clean_word(word)
		references = get_references(word)
		if (references):
			sentences = get_sentences_from_refs(references,word)
			for sentence in sentences:
				print (sentence)
		else:
			print ("No references found")