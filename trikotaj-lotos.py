import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://trikotaj-lotos.ru/catalog/novinki/?list_num=max(5000)')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.select('div.unproduct.one_column')[0]
catalog_list = catalog_wrapper.find_all('article', class_='unproduct-item')

#list to store all data
products = []

# for catalog in tqdm(catalog_list, desc='catalog_list'):
for catalog in tqdm(catalog_list, desc='catalog_list'):
	tag_div = catalog.select('div.unproduct-bottom-container')[0]

	link = 'https://trikotaj-lotos.ru' + tag_div.find('a')['href']
	price = [s for s in (tag_div.find('span', class_='price')).get_text(strip=True).split() if s.isdigit()][0]
	pictures_list = []

	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'html.parser')
	catalog_html = catalog_html.find('main', id='content')

	pictures = catalog_html.find_all('img', class_='img-thumbnail')
	for picture in pictures:
		pictures_list.append('https://trikotaj-lotos.ru' + picture['src'])

	pictures_list = list(set(pictures_list))
	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)