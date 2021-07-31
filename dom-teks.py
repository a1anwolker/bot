import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('http://dom-teks.ru/catalog-news')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.find('div', class_='catalog_all_list')
catalog_list = catalog_wrapper.find_all('div', class_='catalog_list_one')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	tag_a = catalog.select('a')[0]

	link = 'http://dom-teks.ru' + tag_a['href']
	price = (tag_a.select('div.price_catalog>span')[0]).get_text(strip=True)
	pictures_list = []

	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'lxml')
	pictures = catalog_html.find('div', id='gal1').find_all('a')
	for picture in pictures:
		pictures_list.append('http://dom-teks.ru' + picture['data-image'])

	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)
