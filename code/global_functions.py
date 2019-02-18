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

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

def update_global_data_file(global_data):
	try:
		with open("global_data.json","w+") as file:
			json.dump(global_data,file,indent=4)
	except:
		#If there is any kind of error. 
		#We report immediately and restore file from backup
		from shutil import copyfile
		copyfile("global_data_backup.json", "global_data.json")
		return False
	return True

def create_folder(folder_path):
	try:
		if (not os.path.exists(folder_path)):
			os.makedirs(folder_path)
	except:
		return False
	return True

def backup_global_data(global_data):
	from shutil import copyfile
	copyfile("global_data.json","global_data_backup.json")