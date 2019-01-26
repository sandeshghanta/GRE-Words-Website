import os
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
	login_url = "https://manybooks.net/mnybks-login-form"
	# while (r.url == login_url):
	r = requests.get(login_url)
	soup = BeautifulSoup(r.text,"lxml")
	hidden_tags = soup.find_all('input',type='hidden')
	payload = {'email': 'sghanta05@gmail.com', 'pass': 'sandeshghanta047'}
	for tag in hidden_tags:
		payload[tag.get('name')] = tag.get('value')
	print (payload)
	r = requests.post(login_url,data=payload,cookies=r.cookies)
	print (r.url)
	# book_url = "https://manybooks.net/titles/tzusun132132.html"
	# r = requests.get(book_url)
	# print (r.text)

# /mnybks-login-form?ga_submit=lrf%3Abk1P8GWpA5fpWno
