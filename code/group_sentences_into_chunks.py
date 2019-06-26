import os
import json
from global_functions import get_global_data,get_sys_args,update_global_data,create_folder,backup_global_data

if __name__ == "__main__":
	global_data = get_global_data()
	args = get_sys_args()
	args_set = True
	if (len(args) == 0):
		args_set = False
	chunk_max_size = 10000
	for book_source in global_data['sentences_folder_path']:
		if (args_set):
			if (book_source not in args):
				continue
		print ("SOURCE: " + book_source)	#TRACK
		#Used to auto update the global_data.json file. 
		#If a chunk folder path for a source does not exist 
		#it auto adds it to the json obj and later writes it to the file. 
		if (book_source not in global_data['chunks_folder_path']):
			global_data['chunks_folder_path'][book_source] = os.path.join("chunks",book_source)
			result = update_global_data(global_data)
			if (not result):
				print ("FATAL Error, couldn't update global_data.json file. exiting execution of code")
				exit(0)
		result = create_folder(global_data['chunks_folder_path'][book_source])
		if (not result):
			print ("FATAL Error, couldn't create required folders. exiting execution of code")
			exit(0)

		for book_name in os.listdir(global_data['sentences_folder_path'][book_source]):
			print ("Book: " + book_name)	#TRACK
			#splittext is used because book_name will contain a .txt extension, our folder name will not contain it
			chunk_folder_for_book_path = os.path.join(global_data['chunks_folder_path'][book_source],os.path.splitext(book_name)[0])
			sentences_file_path = os.path.join(global_data['sentences_folder_path'][book_source],book_name)
			create_folder(chunk_folder_for_book_path)	#assumed to be error proof
			with open(sentences_file_path,"r") as sentences_of_book:
				chunk_data = ""
				chunk_id = 1
				sentences = sentences_of_book.read().split("::")
				for sentence in sentences:
					if (len(chunk_data) > chunk_max_size):
						chunk_name = "chunk{}.txt".format(chunk_id)
						with open(os.path.join(chunk_folder_for_book_path,chunk_name),"w+") as chunk_file:
							chunk_file.write(chunk_data)
						chunk_id = chunk_id + 1
						chunk_data = sentence
					else:
						if (len(chunk_data) != 0):
							chunk_data += "::"
						chunk_data += sentence

				if (len(chunk_data) > 0):
					chunk_name = "chunk{}.txt".format(chunk_id)
					with open(os.path.join(chunk_folder_for_book_path,chunk_name),"w+") as chunk_file:
						chunk_file.write(chunk_data)