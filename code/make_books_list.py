import os

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

if __name__ == "__main__":
	global_data = get_global_data()
	downloaded_books = {"downloaded":[]}
	for book_name in global_data['books_folder_path']:
		downloaded_books['downloaded'].append(book_name)