import requests
from bs4 import BeautifulSoup

with open('page.html') as f:
    data = f.read()

soup = BeautifulSoup(data)

main_area = soup.find('div', attrs={'class': 'md:grid-cols-3'})

divs = main_area.find_all('a')

names = [div.find('span').text for div in divs]

with open('models.txt', 'w') as f:
    f.write('\n'.join(names))

