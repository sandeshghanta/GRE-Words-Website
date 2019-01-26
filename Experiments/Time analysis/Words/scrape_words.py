from bs4 import BeautifulSoup
import requests
import random
import os
def get_words():
	url = "https://www.vocabulary.com/lists/128536"
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	tags = soup.find_all('a',attrs={'class': 'word dynamictext'})
	word_list = []
	for tag in tags:
		word_list.append(tag.contents[0])
	return word_list

def generate_random_words_file():
	file = open("wordlist.txt","r")
	wordlist = []
	random_words = []
	for word in file:
		wordlist.append(word[:-1])
	for i in range(10000):
		random_words.append(random.choice(wordlist))
	file.close()

	file = open("random_words.txt","w+")
	for word in random_words:
		file.write(word+"\n")
	file.close()

if __name__ == "__main__":
	word_list = get_words()
	file = open("wordlist.txt","w+")
	for word in word_list:
		if ('-' in word or ' ' in word):
			#currently trie is unable to support words like 'avant-garde','high-flown', 'bete noire' etc
			continue
		word = word.lower() #also words should be in lower case
		file.write(word+'\n')
	file.close()
	generate_random_words_file()
