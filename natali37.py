import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://natali37.ru/catalog/products/label/1')
html = BS(req_link.content, 'lxml')

#get max_count of new-products on the site
counter = (html.select('div.products__right-counter.products__counter')[0]).get_text(strip=True)
#load page with max_count of products
req_link = requests.get('https://natali37.ru/catalog/products/label/1' + '?page=1&page_limit=' + [s for s in counter.split() if s.isdigit()][0])
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.select('ul.products__list.list')[0]
catalog_list = catalog_wrapper.find_all('li', class_='product-card')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	tag_a = catalog.select('a.product-card__name.link')[0]

	link = 'https://natali37.ru' + tag_a['href']
	price = [s for s in (catalog.select('div.product-card__price.price')[0]).get_text(strip=True).split() if s.isdigit()][0]
	pictures = (catalog.select('a.swiper-container>div.swiper-wrapper')[0]).find_all('div', class_='swiper-slide')

	pictures_list = []
	for picture in pictures:
		try:
			pictures_list.append(((picture.find('img', class_='image'))['data-src']).replace('thumb.', ''))
		except:
			pictures_list.append(((picture.find('img', class_='image'))['src']).replace('thumb.', ''))

	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)