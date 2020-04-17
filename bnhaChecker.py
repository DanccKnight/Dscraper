#This script checks for a new chapter of MHA. If present, it gets and pushes data to the DB.

import re
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
import time

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
web_url = "https://ww5.readmha.com/chapter/boku-no-hero-academia-chapter-"

docs = db.collection("BNHA").stream()
listnum = []
img_links = []
b = "'[]"

for doc in docs:
    name = doc.id

    #find all numbers and convert to str
    num = re.findall(r'[\d\.\d]+', name)
    num = str(num)

    #remove ''[] chars in num
    for char in b:
        num = num.replace(char,"")
    num = float(num)
    listnum.append(num)

listnum.sort()
l = len(listnum)
last_chapter = listnum[l-1]
new_chapter = last_chapter + 1
#print(last_chapter)

#get the actual link by appending chapter number
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
        print("Chapter not found\nSuspending for 20 minutes...")
        time.sleep(1200)
    else:
        #print(new_chapter)
        #print('Boku no Hero Academia Chapter ' + str(new_chapter))
        data = {
            'number': new_chapter,
            'images': img_links
        }
        try:
            db.collection('BNHA').document('Boku no Hero Academia Chapter ' + str(int(new_chapter))).set(data)
            var = False
            print("Chapter " + str(int(new_chapter)) + " has been added to the database")
        except Exception as ex:
            print(ex)
