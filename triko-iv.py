import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

products = []
domens = [None]*4
domens[0] = 'https://triko-iv.ru/magazin/folder/novinki' # novinki_domen
domens[1] = 'https://triko-iv.ru/magazin/folder/new-dlya-zhenshchin' # women_domen
domens[2] = 'https://triko-iv.ru/magazin/folder/new-dlya-muzhchin' # men_domen
domens[3] = 'https://triko-iv.ru/magazin/folder/new-dlya-detej' # kids_domen

#-----novinki-----
for domen_i in range(len(domens)):
	req_link = requests.get(domens[domen_i])
	html = BS(req_link.content, 'lxml')

	#getting last page num
	last_page = 0
	domen = None
	pages_domen = domens[domen_i] + '/p/'
	try:
		last_page = int(html.find('ul', class_='shop2-pagelist').find_all('li', 'page_num')[-1].find('a').get_text(strip=True))
	except:
		last_page = 1
		
	catalog_list = []

	for i in tqdm(range(last_page)):
		page_req_link = requests.get(pages_domen + str(i))
		page_html = BS(req_link.content, 'lxml')

		catalog_wrapper = html.select('div.product-list')[0]
		catalog_list = catalog_wrapper.find_all('div', class_='product_bot_in1')

		for catalog in catalog_list:
			link = 'https://triko-iv.ru' + catalog.find('div', class_='product_name').find('a')['href']
			price = catalog.find('div', class_='price-current').find('strong').get_text(strip=True)
			pictures_list = []

			#scraping image
			catalog_req_link = requests.get(link)
			catalog_html = BS(catalog_req_link.content, 'lxml')
			pictures = catalog_html.find('div', class_='product_slider_body').find_all('a')
			for picture in pictures:
				pictures_list.append('https://triko-iv.ru' + picture['href'])
			products.append([link, price, pictures_list])

#getting only uniq values from the list products
links = [i[0] for i in products]
new_links = links
links = list(set(links))
new_products = []
uniq_indexes = []

for link in links:
	uniq_indexes.append(new_links.index(link))

for i in uniq_indexes:
	new_products.append(products[i])

for i in new_products:
	print('link: ' + i[0])
	print(' - price: ' + i[1])
	print(' - images: ')
	for j in i[2]:
		print('   * ' + j)