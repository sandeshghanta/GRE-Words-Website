#This script scrapes books from manybooks.net
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def download_book(book_url):
	driver.get(book_url)

def set_profile():
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.download.folderList', 0) # custom location
	profile.set_preference('browser.download.manager.showWhenStarting', False)
	profile.set_preference('browser.download.lastDir', "data/")
	profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/plain")
	profile.set_preference("network.http.response.timeout", 10)
	profile.set_preference("dom.max_script_run_time", 10)
	return profile

def set_option():
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")
	options.binary_location = ""

def login_to_page():
	login_url = "https://manybooks.net/mnybks-login-form"
	driver.get(login_url)
	username = driver.find_element_by_id("edit-email")
	password = driver.find_element_by_id("edit-pass")
	username.send_keys("sghanta05@gmail.com")
	password.send_keys("sandeshghanta047")
	driver.find_element_by_xpath('//*[@id="edit-submit"]').click()
	time.sleep(10)

if __name__ == "__main__":
	profile = set_profile()
	gecko_path = "/home/sharingan/Desktop/Software Engineering/scraper/geckodriver"
	chrome_driver = "/home/sharingan/Desktop/Software Engineering/scraper/chromedriver"
	# driver = webdriver.Firefox(executable_path=gecko_path,firefox_profile=profile)
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.implicitly_wait(10)
	login_to_page()
	page_no = 1
	while (True):
		url = "https://manybooks.net/search-book?field_genre%5B10%5D=10&field_genre%5B62%5D=62&field_genre%5B27%5D=27&field_genre%5B36%5D=36&language=All&search=&sort_by=field_downloads&page={}".format(str(page_no))
		driver.get(url)
		anchor_elements = driver.find_elements_by_xpath("//a[@href]")
		links = []
		for element in anchor_elements:
			links.append(element.get_attribute("href"))
		links = list(set(links))
		for link in links:
			if ("titles" in link):
				print (link)
				driver.get(link)
				inner_links = driver.find_elements_by_xpath("//a[@href]")
				for inner_link in inner_links:
					if ("books/get" in inner_link.get_attribute("href")):
						print (inner_link.get_attribute("href"))
						# p = multiprocessing.Process(target=download_book, args=(inner_link.get_attribute("href"),))
						# p.start()
						# time.sleep(5)
						# p.terminate()
						# p.join()
						driver.get(inner_link.get_attribute("href"))
						break
				driver.back()
		page_no = page_no + 1