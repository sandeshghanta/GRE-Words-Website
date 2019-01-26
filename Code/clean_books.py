import os
import re
from shutil import copyfile

if __name__ == "__main__":
	for file in os.listdir(os.getcwd()+"/books"):
		if not("(" in file and ")" in file):
			copyfile(os.getcwd()+"/books/"+file,os.getcwd()+"/original books/"+file)