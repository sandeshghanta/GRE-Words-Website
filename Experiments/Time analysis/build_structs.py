import os
import json
import random
import pickle

def make_ref():
	user_id = "U" + "".join([str(random.randint(0,9)) for i in range(0,3)])
	book_id = "B" + "".join([str(random.randint(0,9)) for i in range(0,3)])
	chunk_id = "C" + "".join([str(random.randint(0,9)) for i in range(0,3)])
	ref = user_id + book_id + chunk_id
	return ref

class Trie:
	def __init__(self):
		self.root = Node("&")

	# def trav(self):
	# 	q = queue.queue(maxsize=100000000)
	# 	q.put(self.root)
	# 	while (not q.empty()):
	# 		temp = q.get()
	# 		for edge in temp.edges:
	# 			if (edge != None):
	# 				q.put(edge)
	# 		if (len(temp.refs) > 0):
	# 			print 

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
			print ("Word found")
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

def build_trie(words):
	trie = Trie()
	for word in words:
		temp = trie.root
		for char in word:
			t_node = Node(char)
			if (temp.edge_exists(t_node)):
				temp = temp.edges[ord(t_node.char)-97]
			else:
				temp.add_edge(t_node)
				temp = t_node
		temp.add_references()
	return trie

def write_to_file(trie):
	file = open("Trie/trie_data.pk1","wb")
	pickle.dump(trie,file,pickle.HIGHEST_PROTOCOL)
	file.close()

# def read_from_file():
# 	file = open("trie/trie_data.pk1","rb")
# 	trie = pickle.load(file)
# 	file.close()
# 	return trie

def read_wordlist():
	file = open('Words/wordlist.txt','r')
	words = []
	for word in file:
		words.append(word[:-1])
	file.close()
	return words

def make_json_obj_and_write_to_file(trie,words):
	data = {}
	for word in words:
		data[word] = trie.find(word)
	file = open("Json/words.json","w+")
	file.write(json.dumps(data))
	file.close()


if __name__ == "__main__":
	words = read_wordlist()
	trie = build_trie(words)
	write_to_file(trie)
	make_json_obj_and_write_to_file(trie,words)
	del trie
	# trie = read_from_file()
	# while True:
	# 	break
	# 	word = str(input("Enter word "))
	# 	trie.find(word)
