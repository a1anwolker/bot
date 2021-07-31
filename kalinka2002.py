import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

url = 'https://kalinka2002.ru/catalog-news'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'lxml')

links = []
images = []
prices = []

# getting a list of li tags which have products info
links_page = soup.find_all('div', {'class': 'catalog_list_one catalog_list_one_type_0'})
for link_page in tqdm(links_page):
    # appending link to links list
    links.append('https://kalinka2002.ru' + link_page.find('a')['href'])

    # accessing to each page
    url = 'https://kalinka2002.ru' + link_page.find('a')['href']
    req = requests.get(url)
    product_page = BeautifulSoup(req.content, 'lxml')

    # gathering a list of images for one product 
    images_per_product = []
    try:
        for image in product_page.find('div', {'class': 'catalog_add_photos'}).find_all('a'):
            images_per_product.append('https://kalinka2002.ru' + image['data-zoom-image'])
    except:
        images_per_product.append('no image')

    # appending images_per_product list to images list
    images.append(images_per_product)

    # appending prices to list
    prices.append(link_page.find('div', 'toprice').get_text()[:-1].strip())


for link, price, image in zip(links, prices, images):
    print('Link: ', link)
    print('Price: ', price.replace(' ', ''))
    print('Images: ')
    for img in image:
        print(img)
    print('*'*20)