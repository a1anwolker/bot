import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

total_pages = 1
while True:
    url = 'https://ivanovskiy-trikotaj.ru/new/' + f'page={total_pages}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    next_page = soup.find('li', {'class': 'pagination_next_page'})
    if next_page != None:
        total_pages += 1
    else:
        break

links = []
images = []
prices = []
for page_number in tqdm(range(1, total_pages+1)):
    url = 'https://ivanovskiy-trikotaj.ru/new/' + f'page={page_number}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
        
    # getting a list of li tags which have products info
    links_page = soup.find_all('li', {'class': 'position_item position_item_column_4'})
    for link_page in links_page:
        # appending link to links list
        links.append(link_page.find('a', href=True)['href'])

        # accessing to each page
        url = link_page.find('a', href=True)['href']
        req = requests.get(url)
        product_page = BeautifulSoup(req.content, 'lxml')

        # gathering a list of images for one product 
        images_per_product = []
        try:
            for image in product_page.find('ul', {'id': 'product_gallery_box'}).find_all('li'):
                images_per_product.append(image.find('a')['href'])
        except:
            images_per_product.append(product_page.find('div', {'class': 'item_image'}).find('a')['href'])

        # appending images_per_product list to images list
        images.append(images_per_product)

        # appending prices to list
        prices.append(product_page.find('span', {'id': 'page_price_top'}).get_text())


for link, price, image in zip(links, prices, images):
    print('Link: ', link)
    print('Price: ', price.replace(' ', ''))
    print('Images: ')
    for img in image:
        print(img)
    print('*'*20)