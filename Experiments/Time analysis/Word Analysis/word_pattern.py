import os
import matplotlib.pyplot as plt

def read_words():
	file = open(os.path.dirname(__file__) + "../Words/wordlist.txt","r")
	words = []
	for word in file:
		words.append(word[:-1])
	file.close()
	return words

def analyse_length(words):
	len_data = {}
	for word in words:
		if len(word) in len_data:
			len_data[len(word)] = len_data[len(word)] + 1
		else:
			len_data[len(word)] = 1
	lengths = []
	count = []
	for length in len_data:
		lengths.append(length)
		count.append(len_data[length])
	plt.plot(lengths, count)
	plt.show()

def analyse_start_letter(words):
	start_letter_data = {}
	for i in range(0,27):
		start_letter_data[chr(i+97)] = 0

	for word in words:
		start_letter_data[word[0]] = start_letter_data[word[0]] + 1

	letters = []
	count = []
	for i in range(0,27):
		count.append(start_letter_data[chr(i+97)])
		letters.append(chr(i+97))
	plt.plot(letters,count)
	plt.show()

if __name__ == "__main__":
	words = read_words()
	analyse_start_letter(words)