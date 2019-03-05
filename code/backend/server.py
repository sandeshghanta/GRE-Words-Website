import os
import json
import requests
from flask import Flask
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
#mongo contains reference to the words db
mongo = MongoClient('mongodb://127.0.0.1:27017').words

def get_global_data():
	#This function reads the global_data json file
	with open("global_data.json","r") as file:
		global_data = json.load(file)
	return global_data

@app.route('/clear_data', methods=['GET','POST'])
def clear_data():
	print (mongo.dbPath)
	mongo.words.delete_many({})
	return json.dumps({"Success":True}), 200, {'ContentType':'application/json'}

@app.route('/add_data', methods=['GET','POST'])
def add_data():
	global_data = get_global_data()
	for i in range(26):
		json_file_name = "{}_words.json".format(chr(97+i))
		json_file_path = os.path.join(global_data['json_folder_path'],json_file_name)
		json_data = {}
		with open(json_file_path,'r') as json_file:
			json_data = json.load(json_file)
		for word in json_data:
			mongo.words.insert_one({"word":word,"refs":json_data[word]})
	mongo.words.create_index([("word",1)], unique=True )
	return json.dumps({"Success":True}), 200, {'ContentType':'application/json'}

@app.route('/display_data', methods=['GET','POST'])
def display_data():
	cursor = mongo.words.find({})
	result = []
	for document in cursor:
		result.append({"word":document['word'],"refs":document['refs']})
	return json.dumps(result), 200, {'ContentType':'application/json'}

@app.route('/search/<string:query>', methods=['GET','POST'])
def search(query):
	result = mongo.words.find_one({ "word" : query })
	sentences = get_sentences_from_refs(result['refs'])
	return json.dumps(sentences), 200, {'ContentType':'application/json'}

def get_sentences_from_refs(refs):
	global_data = get_global_data()
	sentences = []
	for ref in refs:
		source,book_id,chunk_id,sentence_no = ref.split("::")
		chunk_path = os.path.join(global_data['chunks_folder_path'][source],book_id,chunk_id)
		with open(chunk_path,'r') as chunk:
			chunk_data = chunk.readline()
			sentences_in_chunk = chunk_data.split("::")
			sentences.append(sentences_in_chunk[int(sentence_no)])
	return sentences

if __name__ == '__main__':
	app.run(debug=True)