import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://homestyle-iv.ru/new')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.find('div', id='count_prod')
catalog_list = catalog_wrapper.find_all('div', class_='prod')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	link = 'https://homestyle-iv.ru' + catalog.select('div.name_prod>a')[0]['href']
	price = [s for s in catalog.select('div.name_prod2>div.name_prod2>table>tbody>tr')[0].select('td')[0].select('div.price_prod')[0].get_text(strip=True).split() if s.isdigit()][0]
	pictures_list = []

	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'lxml')
	pictures = catalog_html.select('div.bol')[0].find_all('img')
	for picture in pictures:

		if 'http' in picture['src']:
			pictures_list.append(picture['src'])
		else:
			pictures_list.append('https://homestyle-iv.ru' + picture['src'])

	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)