import os

if __name__ == "__main__":
	for book in os.listdir(os.getcwd()+"/original books/"):
		file = open(os.getcwd()+"/original books/" + book,"r")
		