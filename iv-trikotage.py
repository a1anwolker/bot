import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm
import os

req_link = requests.get('https://iv-trikotage.ru/shop/novinki/?sort=create_datetime&order=asc')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.select('div.product-list')[0]
catalog_list = catalog_wrapper.find('div', class_='row')
catalog_list = catalog_list.select('div#produkt')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	tag_a = catalog.select('div.slide.produkt>a')[0]
	
	link  = 'https://iv-trikotage.ru' + tag_a['href']
	price = [s for s in tag_a.find('span').get_text(strip=True).split() if s.isdigit()][1]
	pictures_list = []

	#scraping image
	catalog_req_link = requests.get(link)
	catalog_html = BS(catalog_req_link.content, 'html.parser')
	catalog_html = catalog_html.select('div.gallery')[0]

	pictures = catalog_html.find_all('img', class_='')
	for picture in pictures:
		picture_ext = os.path.splitext(picture['src'])


		pictures_list.append('https://iv-trikotage.ru' + picture_ext[0] + '@2x' + picture_ext[1])
	products.append([link, price, pictures_list])


for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)