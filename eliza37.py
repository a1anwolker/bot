import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('http://eliza37.ru/catalog-news')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.select('div.catalog_all_list')[0]
catalog_list = catalog_wrapper.find_all('div', class_='catalog_list_one')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	tag_a = catalog.select('a')[0]

	link = 'http://eliza37.ru' + tag_a['href']
	price = tag_a.find('p', class_='price_catalog')
	for drop_span_tag in price.findAll('span'):
		drop_span_tag.replace_with('')
	price = [s for s in price.get_text().split() if s.isdigit()][0]
	pictures_list = []

	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'lxml')
	pictures = catalog_html.find('div', id='gal1').find_all('a')
	for picture in pictures:
		pictures_list.append('https://eliza37.ru' + picture['data-image'])

	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)