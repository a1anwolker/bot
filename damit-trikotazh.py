import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

req_link = requests.get('https://damit-trikotazh.ru/172')
html = BS(req_link.content, 'lxml')

#getting last page num
last_page = int(((html.find('div', class_='pagination').find('ul').find_all('li')[-1]).find('a'))['href'].split('=')[-1])
domen = 'https://damit-trikotazh.ru/172/page='
catalog_list = []

#list to store all data
products = []

#parsing pages
for page in tqdm(range(1, last_page+1)):
	page_req_link = requests.get(domen + str(page))
	page_html = BS(page_req_link.content, 'lxml')

	ul_tag = page_html.find('ul', id='cat_card')
	catalog_list = ul_tag.find_all('div', class_='position_item_container')
	
	for catalog in catalog_list:
		link = 'https://damit-trikotazh.ru' + (catalog.find_all('a')[0])['href']
		price = (catalog.select('div.item_content>span.cennik')[0]).get_text().split()[0].strip()
		pictures_list = []

		#scraping image
		catalog_req_link = requests.get(link)
		catalog_html = BS(catalog_req_link.content, 'lxml')
		try:
			pictures = catalog_html.find('ul', id='product_gallery_box').find_all('a', class_='litebox-zoom-gallery')
			for picture in pictures:
				pictures_list.append(picture['href'])
		except:
			pictures_list.append(catalog_html.find('a', id='litebox_image_container_product')['href'])
		products.append([link, price, pictures_list])

for i in products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)