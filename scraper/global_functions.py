import os
import sys
import json

def get_sys_args():
	args = []
	if (len(sys.argv) > 1):
		if (sys.argv[1] == "--compile" or sys.argv[1] == "-c"):
			if (len(sys.argv) > 2):
				args = sys.argv[2:]
	return args

def is_relevant_sentence(sentence,word):
	#IMPROVE have to write relevant code here.
	return True

def is_text(text):
	if (len(text) == 0):
		return False
	for char in text: #return True if atleast one alphabet is there
		if (ord(char) >= 65 and ord(char) <= 90):
			return True
		if (ord(char) >= 97 and ord(char) <= 122):
			return True
	return False

def add_reference(word,path_to_sentence):
	word = word.lower()
	global_data = get_global_data()
	if (ord(word[0]) < 97 or ord(word[0]) > 122):
		print ("Invalid Word ",word)   #LOG
		return
	data = {}
	with open(os.path.join(global_data['json_folder_path'],"{}_words.json".format(word[0])),'r') as file:
		data = json.load(file)
		if (word not in data):
			print ("Word not found ",word)	#LOG
			return
		data[word].append(path_to_sentence)
	
	with open(os.path.join(global_data['json_folder_path'],"{}_words.json".format(word[0])),'w+') as file:
		json.dump(data,file,indent=4)

def remove_file(file_path):
	if (os.path.exists(file_path)):
		os.remove(file_path)
	else:
		print ("File does not exist")	#LOG

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

def update_global_data(global_data):
	try:
		with open("global_data.json","w+") as file:
			json.dump(global_data,file,indent=4)
	except:
		#If there is any kind of error. 
		#We report immediately and restore file from backup
		from shutil import copyfile
		copyfile("global_data_backup.json", "global_data.json")
		return False
	backup_global_data()
	return True

def backup_global_data():	#Assumed to be error proof
	from shutil import copyfile
	copyfile("global_data.json","global_data_backup.json")

def get_wordlist(json_format=False):
	#If json_format = True then function returns a json obj of the wordlist in the format {word1:True,word2:True}
	#This is used when we have to search for a particular word. Complexity for searching in json obj is O(1) for list it is O(N)
	global_data = get_global_data()
	with open(global_data['wordlist_file_path'],'r') as wordlist_file:
		wordlist = wordlist_file.read().split('::')
	if (json_format):
		true_list = [True for i in range(len(wordlist))]
		return dict(zip(wordlist,true_list))
	else:
		return wordlist

def create_folder(folder_path):
	try:
		if (not os.path.exists(folder_path)):
			os.makedirs(folder_path)
	except:
		return False
	return True