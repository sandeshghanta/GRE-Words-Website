import json
from global_functions import get_global_data,get_wordlist

def ovveride_refs(wordlist):
	data = [{} for i in range(0,26)]
	for word in wordlist:
		data[ord(word[0])-97][word] = []
	char = 'a'
	for lis in data:
		try:
			with open("{}/{}_words.json".format(global_data['json_folder_path'],char),"w+") as file:
				json.dump(lis,file,indent=4)
		except:
			return False
		char = chr(ord(char)+1)
	return True

if __name__ == "__main__":
	global_data = get_global_data()
	wordlist = get_wordlist()
	result = ovveride_refs(wordlist)
	if (result):
		print ("Overrode all references to all words")
	else:
		print ("Unable to override references, data might be partially overrode!")