import os
import time
import json
#For 100 words time taken is 11.90 seconds
def read_json_from_file():
	file = open("words.json","r")
	json_data = json.load(file)
	file.close()
	return json_data

if __name__ == "__main__":
	file = open(os.path.dirname(__file__) + "../Words/random_words.txt","r")
	random_words = []
	for word in file:
		random_words.append(word[:-1])
	random_words = random_words[0:100]
	file.close()
	start_time = time.time()
	for word in random_words:
		file = open("words.json","r")
		json_data = json.load(file)
		x = json_data[word]
		file.close()
	print ("time taken is " + str(time.time()-start_time))