import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

web_url = 'https://ww5.readmha.com/manga/boku-no-hero-academia/'

r = requests.get(web_url)
soup = BeautifulSoup(r.text,'html.parser')
links_set = soup.find_all('a', class_ = "text-gray-900 dark:text-white text-lg font-semibold mb-1")

chapter_links = []
image_links = []

for link in links_set:
    chapter_links.append(str(link['href']))

var = len(chapter_links) + 1

for link in chapter_links:
    print("Chapter ->" + link)
    web_url = link
    r = requests.get(web_url)
    soup = BeautifulSoup(r.text,'html.parser')
    img_set = soup.find_all('img', class_ = "my-3 mx-auto js-page")
    for x in img_set:
        image_links.append(str(x['src']))
    print("Image ->")
    for x in image_links:
        print(x)

#    print(str(var) + ":" + link)
#    db.collection('My Hero Academia').document('Chapter ' + str(var)).
