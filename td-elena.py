import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

url = 'https://td-elena.ru/catalog/novinki/'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'lxml')

total_pages = int(soup.find('span', {'class': 'nums'}).find_all('a')[-2].get_text())

links = []
images = []
prices = []
for page in tqdm(range(1, total_pages+1)):
    url = f'https://td-elena.ru/catalog/novinki/?PAGEN_1={page}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
      
    # getting a list of li tags which have products info
    links_page = soup.find_all('div', {'class': 'catalog_item_wrapp'})
    for link_page in links_page:
        # appending link to links list
        links.append('https://td-elena.ru' + link_page.find_all('a')[1]['href'])

        # accessing to each page
        url = 'https://td-elena.ru' + link_page.find_all('a')[1]['href']
        req = requests.get(url)
        product_page = BeautifulSoup(req.content, 'lxml')

        # gathering a list of images for one product 
        images_per_product = []
        if len(product_page.find('div', {'class': 'img_wrapper'}).find_all('img', {'data-slide-index': lambda x: x == None})) != 0:
            for image in product_page.find('div', {'class': 'img_wrapper'}).find_all('img', {'data-slide-index': lambda x: x == None}):
                images_per_product.append('https://td-elena.ru' + image['src'])
        else:
            images_per_product.append('no images')

        # appending images_per_product list to images list
        images.append(images_per_product)

        # appending prices to list
        prices.append(product_page.find('span', {'class': 'price-val'}).get_text().strip())


for link, price, image in zip(links, prices, images):
    print('Link: ', link)
    print('Price: ', price.replace(' ', ''))
    print('Images: ')
    for img in image:
        print(img)
    print('*'*20)