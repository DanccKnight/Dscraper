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
last_chapter = listnum[-1]
new_chapter = last_chapter + 1

web_url = web_url + str(int(last_chapter + 1))

r = requests.get(web_url)
soup = BeautifulSoup(r.text,'html.parser')

for link in soup.find_all('img', class_ = "my-3 mx-auto js-page"):
    content = str(link['src'])
    size = len(content)

    #get rid of fraudulent links
    if(content[len(content)-1] == 0):
        continue
    else:
        for k in range(size-6):
            if content[k] == 'l' and content[k+1] == '=' and content[k+2] == 'h' and content[k+3] == 't' and content[k+4] == 't':
                sliced_string = content[k+2:size]
                img_links.append(sliced_string)
                continue

    img_links.append(content)

var = True
while var:
    if(len(img_links) < 4):
        print("Chapter " + str(int(new_chapter)) + " not found\n")
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

