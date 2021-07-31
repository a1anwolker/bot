import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://darinatex.ru/catalog-news/')
html = BS(req_link.content, 'lxml')

#getting last page num
last_page = int(html.find('div', class_='pagination').find('ul', class_='pag').find('li', class_='last').find('a')['href'].split('=')[1])
domen = 'https://darinatex.ru/catalog-news/?page='

#list to store all data
products = []

#parsing pages
for page in tqdm(range(1, last_page+1)):
	page_req_link = requests.get(domen + str(page))
	page_html = BS(page_req_link.content, 'lxml')

	catalog_wrapper = page_html.find('div', id='content').select('div.product-wrap')[0]
	catalog_list = catalog_wrapper.find_all('div', class_='product')

	for catalog in catalog_list:
		link = catalog.select('div.image>a')[0]['href']
		price = ''
		try:
			price = catalog.select('div.caption>div.price>span.price-number')[0].get_text(strip=True)
		except:
			price = '0'
		pictures_list = []
		 #scraping image
		pictures_list.append(catalog.select('div.image>a>img.img-responsive')[0]['src'].replace('267x400', '490x715'))
		products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)