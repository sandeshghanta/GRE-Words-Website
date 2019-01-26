import pickle
import time
import os
#100 random words took 130.61 seconds
def read_from_file():
	file = open("trie_data.pk1","rb")
	trie = pickle.load(file)
	file.close()
	return trie

class Trie:
	def __init__(self):
		self.root = Node("&")

	def find(self,word):
		temp = self.root
		found = True
		for char in word:
			temp = temp.edges[ord(char)-97]
			if (temp == None):
				found = False
				print ("ERROR: " + word + " not found")
				break
		if (found):
			return temp.refs


class Node:
	def __init__(self,x):
		self.char = x
		self.edges = [None]*26
		self.refs = []
	
	def add_edge(self,next_node):
		self.edges[ord(next_node.char)-97] = next_node

	def edge_exists(self,next_node):
		if (self.edges[ord(next_node.char)-97] == None):
			return False
		return True

	def add_references(self):
		count = random.randint(1,100)
		for i in range(count):
			self.refs.append(make_ref())

if __name__ == "__main__":
	#trie = read_from_file()
	file = open(os.path.dirname(__file__) + "../Words/random_words.txt","r")
	random_words = []
	for word in file:
		random_words.append(word[:-1])
	random_words = random_words[:100]
	file.close()
	start_time = time.time()
	for word in random_words:
		file = open("trie_data.pk1","rb")
		trie = pickle.load(file)
		file.close()
		x = trie.find(word)
	print ("time taken is " + str(time.time()-start_time))