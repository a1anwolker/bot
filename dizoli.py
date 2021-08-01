import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#chromeOptions
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
login = 'lotot78421@drawings101.com'
password = '123456789'

domen = 'https://dizoli.ru/catalog/'
driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
driver.get(domen)
sleep(2)

#look for log_in button
driver.find_element_by_css_selector('a.header-links__link.user-icon').click()
# sleep(2)

#look for input areas
driver.find_element_by_name('USER_LOGIN').send_keys(login)
driver.find_element_by_name('USER_PASSWORD').send_keys(password)

#look for enter button
driver.find_element_by_name('Login').click()
sleep(2)

#redirection to the catalog page
driver.get(domen)
sleep(5)

#scroll down until the end of the page
for _ in range(5):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(2)

#getting the source of the page
html = BS(driver.page_source, 'lxml')

#list to store all data
products = []

catalog_wrapper = html.find('div', id='comp_150d527eb2d9a0f2bb3cc0d8d6a2170d').select('div.catalog-list')[0]
catalog_list = catalog_wrapper.find_all('div', class_='catalog-list__col')

for catalog in tqdm(catalog_list):
	link = 'https://dizoli.ru' + catalog.select('div.element-card__name>a')[0]['href']
	price = [s for s in catalog.select('div.element-card__price')[0].get_text(strip=True).split() if s.isdigit()][0]
	pictures_list = []

	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'lxml')

	pictures1 = catalog_html.find('div', class_='element-block').find('div', class_='element-images-min').find_all('a')
	for picture in pictures1:
		pictures_list.append('https://dizoli.ru' + picture['href'])
	
	pictures2 = catalog_html.find('div', class_='element-block').find_all('div', class_='element-color-images')
	for picture in pictures2:
		image_link = picture.find('div', class_='element-images__item').find('a')['href']
		if image_link not in pictures_list:
			pictures_list.append('https://dizoli.ru' + image_link)

	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)

