import re
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials,firestore
import time

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
web_url = "https://ww4.readhaikyuu.com/chapter/haikyuu-chapter-"

docs = db.collection("Haikyuu").stream()
listnum = []
img_links = []
b = "'[]"

for doc in docs:
    name = doc.id

    num = re.findall(r'[\d\.\d]+',name)
    num = str(num)

    for char in b:
        num = num.replace(char,"")
    num = float(num)
    listnum.append(num)

listnum.sort()
l = len(listnum)
last_chapter = listnum[l-1]
new_chapter = last_chapter + 1

web_url = web_url + str(int(last_chapter + 1))

r = requests.get(web_url)
soup = BeautifulSoup(r.text,'html.parser')

for link in soup.find_all('img', class_ = "my-3 mx-auto js-page"):
    content = str(link['src'])
    if(content[len(content)-1] == 0):
        continue
    img_links.append(str(content))

var = True
while var:
    if(len(img_links) < 4):
        print("Chapter " + str(int(new_chapter)) + " not found\nSuspending for 20 minutes...")
        time.sleep(1200)
    else:

        data = {
            'number': new_chapter,
            'images': img_links

        }

        try:
            db.collection('Haikyuu').document('Haikyuu Chapter ' + str(int(new_chapter))).set(data)
            var = False
            print("Database updated")
        except Exception as ex:
            print(ex)

