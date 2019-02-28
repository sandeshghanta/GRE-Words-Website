import os
import json
import requests
from bs4 import BeautifulSoup
from global_functions import get_global_data
#https://www.gutenberg.org/wiki/Category:History_Bookshelf
#https://www.gutenberg.org/wiki/Category:Law_Bookshelf
urls = ["https://www.gutenberg.org/wiki/Category:Technology_Bookshelf","https://www.gutenberg.org/wiki/Category:Science_Bookshelf","https://www.gutenberg.org/wiki/Category:Social_Sciences_Bookshelf","https://www.gutenberg.org/wiki/Category:Social_Sciences_Bookshelf"]

def download_book(link,book_id):
	if ("http:" not in link):	#some links are like //www.gutenberg.org/files/17321/17321-0.txt
		link = "http:" + link
	r = requests.get(link)
	book_name = book_id + ".txt"
	try:
		with open(os.path.join(global_data['books_folder_path']["gutenberg"],book_name),"w+") as book:
			book.write(r.text)
		return True
	except:		#some error happened
		return False

def scrape_book(link):
	if ("http:" not in link):	#some links are like //www.gutenberg.org/ebooks/17321
		link = "http:" + link
	book_id = link[link.rfind('/')+1:]		#to get the book_id i.e 17321
	r = requests.get(link)
	soup = BeautifulSoup(r.text,"lxml")
	all_links = soup.find_all('a')
	for link in all_links:
		try:
			if (".txt" in link['href']):
				result = download_book(link['href'],book_id)
				if (result):
					print ("downloaded {}".format(book_id))
				else:
					print ("ERROR couldn't download {}".format(book_id))
		except KeyError:
			do_nothing = 1

def scrape_all_books(link):
	r = requests.get(link)
	soup = BeautifulSoup(r.text,"lxml")
	all_links = soup.find_all('a')
	for link in all_links:
		try:
			if ("ebooks" in link['href']):
				scrape_book(link['href'])		
		except KeyError:		#some anchor tags might be pointing to elements in page <a id="top">link</a>
			do_nothing = 1

if __name__ == "__main__":
	global_data = get_global_data()
	for url in urls:
		print (url)
		r = requests.get(url)
		soup = BeautifulSoup(r.text,"lxml")
		div = soup.find("div",{"id":"mw-pages"})
		all_links = div.find_all('a')
		for link in all_links:
			scrape_all_books("https://www.gutenberg.org"+link['href'])
			print (link['href'])