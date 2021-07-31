import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://dom-trikotazha.ru/novinki')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.find('div', id='content')
catalog_list = catalog_wrapper.find_all('div', class_='caption')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	link = (catalog.select('a')[0])['href']
	price = ''.join([s for s in (catalog.select('div.dicount-price>div')[0]).select('span')[1].get_text(strip=True).split() if s.isdigit()])
	pictures_list = []
	
	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'lxml')
	pictures = catalog_html.find('div', id='content').find('ul', class_='thumbnails').find_all('a', class_='thumbnail')
	for picture in pictures:
		pictures_list.append(picture['href'])

	products.append([link, price, pictures_list])


for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)