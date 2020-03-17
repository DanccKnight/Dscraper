import requests
from bs4 import BeautifulSoup

url = 'https://ww5.readmha.com/manga/boku-no-hero-academia/'

r = requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')
links = soup.find_all('a',class_="text-gray-900 dark:text-white text-lg font-semibold mb-1")

for link in links:
    print(link['href'])
