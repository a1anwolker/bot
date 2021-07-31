import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

url = 'https://iv-capriz.com/shop/populjarnoe'
req = requests.get(url)

soup = BeautifulSoup(req.content,'lxml')

total_pages = int(soup.find('span', {'class': 'plist'}).find_all('span')[-1].get_text())

links = []
images = []
prices = []
pbar = tqdm(total=total_pages)
for page in range(1, total_pages+1):
    url = f'https://iv-capriz.com/shop/populjarnoe;{page}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    
    if req.status_code == 404:
        url = f'https://iv-capriz.com/shop/populjarnoe'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
      
    # getting a list of li tags which have products info
    links_page = soup.find_all('div', {'class': 'list-item'})
    for link_page in links_page:
        # appending link to links list
        links.append('https://iv-capriz.com' + link_page.find('table').find('a')['href'])

        # accessing to each page
        url = 'https://iv-capriz.com' + link_page.find('table').find('a')['href']
        req = requests.get(url)
        product_page = BeautifulSoup(req.content, 'lxml')

        # gathering a list of images for one product 
        images_per_product = []
        if len(product_page.find_all('div', {'class': 'ienlarger'})) != 0:
            for image in product_page.find_all('div', {'class': 'ienlarger'}):
                images_per_product.append('https://iv-capriz.com' + image.find('a')['href'])
        else:
            images_per_product.append('https://iv-capriz.com' + product_page.find('td', {'style': 'padding-right:10px; width:1%'}).find('img')['src'])

        # appending images_per_product list to images list
        images.append(images_per_product)

        # appending prices to list
        prices.append(product_page.find('span', {'class': lambda n: n and 'id-' in n}).get_text())

    # tqdm
    pbar.update(1)
pbar.close()

for links, price, image in zip(links, prices, images):
    print('Links: ', links)
    print('Price: ', price)
    for img in image:
        print(img)
    print('-'*50)