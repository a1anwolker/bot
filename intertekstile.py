import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

url = 'https://intertekstile.ru/catalog/a_novinki'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'lxml')

total_pages = int(soup.find('div', {'class': 'nums'}).find_all('a')[-1].get_text())

links = []
images = []
prices = []
for page in tqdm(range(1, total_pages+1)):
    url = f'https://intertekstile.ru/catalog/a_novinki/?PAGEN_1={page}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
      
    # getting a list of li tags which have products info
    links_page = soup.find_all('div', {'class': 'catalog_item_wrapp'})
    for link_page in links_page:
        # appending link to links list
        links.append('https://intertekstile.ru' + link_page.find_all('a')[1]['href'])

        # accessing to each page
        url = 'https://intertekstile.ru' + link_page.find_all('a')[1]['href']
        req = requests.get(url)
        product_page = BeautifulSoup(req.content, 'lxml')

        try:
            images.append('https://intertekstile.ru' + product_page.find('div', {'class': 'offers_img wof'}).find('a')['href'])
        except:
            images.append('no images')

        # appending prices to list
        try:
            prices.append(link_page.find('span', {'class': 'price_value'}).get_text())
        except:
            prices.append('Нет в наличии')

for link, price, image in zip(links, prices, images):
    print('Link: ', link)
    print('Price: ', price)
    if 'javascript' in image:
        print('Images: ', '')
    else:
        print('Images: ', image)
    print('*'*20)