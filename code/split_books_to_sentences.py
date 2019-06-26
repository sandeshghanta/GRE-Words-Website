import os
import json
import random
from global_functions import get_global_data,get_sys_args,update_global_data,create_folder,backup_global_data
from nltk import tokenize


def get_sentences(text):
	return tokenize.sent_tokenize(text)


if __name__ == "__main__":
	args = get_sys_args()
	args_set = True
	if (len(args) == 0):
		args_set = False
	global_data = get_global_data()
	for book_source in global_data['books_folder_path']:
		if (args_set):
			if (book_source not in args):
				continue
		print ("SOURCE: " + book_source)	#TRACK
		# Used to auto update the global_data.json file.
		# If a sentence folder path for a source does not exist
		# it auto adds it to the json obj and later writes it to the file.
		if (book_source not in global_data['sentences_folder_path']):
			global_data['sentences_folder_path'][book_source] = os.path.join("sentences", book_source)
			result = update_global_data(global_data)
			if (not result):
				print ("FATAL Error, couldn't update global_data.json file. exiting execution of code")
				exit(0)
		result = create_folder(global_data['sentences_folder_path'][book_source])
		if (not result):
			print ("FATAL Error, couldn't create required folders. exiting execution of code")
			exit(0)

		for book_name in os.listdir(global_data['books_folder_path'][book_source]):
			print ("Book: " + book_name)	#TRACK
			with open(os.path.join(global_data['books_folder_path'][book_source],book_name),"r") as book:
				text = book.read()
				sentences = get_sentences(text)
				with open(os.path.join(global_data['sentences_folder_path'][book_source],book_name),"w+") as file:
					for sentence in sentences:
						if (sentence == "" or sentence == "\n" or len(sentence) == 0):
							continue
						sentence = sentence.replace("\n","")
						file.write(sentence+"::")
					try:
						file.seek(file.tell() - 2, os.SEEK_SET)	#the last sentence will also be ending with "::", as that might cause problems in the future we are removing them here itself
						file.write('')
					except:
						print ("File has no data")		#LOG write this to error file