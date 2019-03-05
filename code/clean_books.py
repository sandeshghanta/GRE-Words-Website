import os
import re
from shutil import copyfile
#Code not needed anymore
if __name__ == "__main__":
	for file in os.listdir(os.getcwd()+"/books"):
		if not("(" in file and ")" in file):
			copyfile(os.getcwd()+"/books/"+file,os.getcwd()+"/original books/"+file)