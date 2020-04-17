import re
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
num = 265
web_url = 'https://ww5.readmha.com/chapter/boku-no-hero-academia-chapter-' + str(num)

r = requests.get(web_url)
soup = BeautifulSoup(r.text,'html.parser')
img_links = []

for i in soup.find_all('img', class_ = "my-3 mx-auto js-page"):
    content = str(i['src'])
    #if(content[len(content)-1] == '0'):
    #    continue
    img_links.append(content)
    print(content)

data = {
    'number': num,
    'images': img_links
  }

#db.collection('BNHA').document("Boku no Hero Academia Chapter " + str(num)).set(data)
