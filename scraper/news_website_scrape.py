import os
import requests
from bs4 import BeautifulSoup

text = []
not_accepted_tags = ["script","a","button","img","style","code"]
def is_text(text):
	if (len(text) == 0):
		return False
	if (len(text.split(" ")) <= 5):
		return False
	return True

def traverse_tree(soup,parent_name):
	try:
		for child in soup.children:
			traverse_tree(child,soup.name)
	except AttributeError:
		soup = soup.replace('\t','')
		soup = soup.replace('\n','')
		soup = soup.strip(' ')
		if (is_text(soup) and parent_name not in not_accepted_tags):
			text.append(soup)
			# print (soup,parent_name)

if __name__ == "__main__":
	url = "https://www.npr.org/2019/02/15/694897468/trump-wants-to-use-iraqi-base-to-watch-iran-now-iraqi-parties-want-u-s-forces-ou"
	r = requests.get(url)
	# print (r.text)
	soup = BeautifulSoup(r.text,"lxml")
	# r = open("scraper/output.html","r")
	soup = BeautifulSoup(r.read(),"lxml")
	traverse_tree (soup.body,soup.name)
	text = " ".join(text)
	print (text)