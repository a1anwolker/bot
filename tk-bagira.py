import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

total_pages = 1
while True:
    url = f'https://tk-bagira.ru/new-trik/?yclid=0&PAGEN_2={total_pages}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    next_page = soup.find('li', {'class': 'bx-pag-next'}).find('a')
    if next_page != None:
        total_pages += 1
    else:
        break

links = []
images = []
prices = []
for page_number in tqdm(range(1, total_pages+1)):
    url = f'https://tk-bagira.ru/new-trik/?yclid=0&PAGEN_2={page_number}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
        
    # getting a list of li tags which have products info
    links_page = soup.find_all('div', {'class': 'catalog-item col-4 xs-col-6'})
    for link_page in links_page:
        # appending link to links list
        links.append('https://tk-bagira.ru' + link_page.find('div', {'class': 'element rag'}).find('a')['href'])

        # accessing to each page
        url = 'https://tk-bagira.ru' + link_page.find('div', {'class': 'element rag'}).find('a')['href']
        req = requests.get(url)
        product_page = BeautifulSoup(req.content, 'lxml')

        # gathering a list of images for one product 
        images_per_product = []
        try:
            for image in product_page.find_all('a', {'class': 'fancy'}):
                images_per_product.append('https://tk-bagira.ru' + image.find('img')['src'])
        except:
            images_per_product.append('no image')

        # appending images_per_product list to images list
        images.append(images_per_product)

        # appending prices to list
        prices.append(link_page.find('div', {'class': 'element-cena row'}).get_text().strip().strip(' руб.'))


url = 'https://tk-bagira.ru/new-teks'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'lxml')

# getting a list of li tags which have products info
links_page = soup.find('div', {'class': 'columns xs-columns-min'}).find_all('div', {'class': 'element'})
for link_page in tqdm(links_page):
    # appending link to links list
    links.append('https://tk-bagira.ru' + link_page.find('a')['href'])

    # accessing to each page
    url = 'https://tk-bagira.ru' + link_page.find('a')['href']
    req = requests.get(url)
    product_page = BeautifulSoup(req.content, 'lxml')

    # gathering a list of images for one product 
    images_per_product = []
    try:
        for image in product_page.find_all('a', {'class': 'fancy'}):
            images_per_product.append('https://tk-bagira.ru' + image.find('img')['src'])
    except:
        images_per_product.append('no image')

    # appending images_per_product list to images list
    images.append(images_per_product)

    # appending prices to list
    prices.append(link_page.find('div', {'class': 'element-cena row'}).get_text().strip().strip(' руб.'))


for link, price, image in zip(links, prices, images):
    print('Link: ', link)
    if price.startswith('Вед'):
        print('Price: ', price)
    else:
        print('Price: ', price.replace(' ', ''))
    print('Images: ')
    for img in image:
        print(img)
    print('*'*20)