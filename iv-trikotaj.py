import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://iv-trikotaj.ru/')
html = BS(req_link.content, 'lxml')

catalog_wrapper = html.select('div.bg-carousel.panel-default')
#getting index of new catalog from the list of catalogs
print(len(catalog_wrapper))
index_of_new = 0
for i in range(len(catalog_wrapper)):
	if catalog_wrapper[i].select('div.panel-heading>h4.panel-title')[0].get_text(strip=True)=='Новинки':
		index_of_new = i
		break
catalog_list = catalog_wrapper[index_of_new].find_all('div', class_='product-block')

#list to store all data
products = []

for catalog in tqdm(catalog_list, desc='catalog_list'):
	new_catalog = catalog.select('div.product-meta')[0]
	link = new_catalog.select('h6.name>a')[0]['href']
	price = [s for s in new_catalog.select('div.price>span.price-olds')[0].get_text(strip=True).split() if s.isdigit()][0]
	pictures_list = []

	#scraping image
	try:
		catalog_req_link = requests.get(link)
		catalog_html = BS(catalog_req_link.content, 'lxml')
		pictures = catalog_html.find('div', id='image-additional-carousel').find_all('a')
		for picture in pictures:
			pictures_list.append('https://iv-trikotaj.ru' + picture['href'])
	except:
		picture = catalog.select('div.product-img>a>img')[0]
		pictures_list.append(picture['src'])

	products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)