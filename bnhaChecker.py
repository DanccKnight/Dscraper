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
last_chapter = listnum[-1]
new_chapter = last_chapter + 1
#print(last_chapter)

#get the actual link by appending chapter number
web_url = web_url + str(int(new_chapter))

r = requests.get(web_url)
soup = BeautifulSoup(r.text,'html.parser')

for link in soup.find_all('img', class_ = "my-3 mx-auto js-page"):
    content = str(link['src'])
    size = len(content)

    #get rid of fraudulent links
    if content[size-1] == 0:
        continue
    else:
        for k in range(size-6):
            if content[k] == 'l' and content[k+1] == '=' and content[k+2] == 'h' and content[k+3] == 't' and content[k+4] == 't':
                sliced_string = content[k+2:size]
                img_links.append(sliced_string)
                continue

    img_links.append(content)

#var = True
#while var:
if len(img_links) < 4:
    print("Chapter " + str(int(new_chapter)) + " not found\n")
else:
    #print(new_chapter)
    #print('Boku no Hero Academia Chapter ' + str(new_chapter))
    data = {
        'number': new_chapter,
        'images': img_links
    }
    try:
        db.collection('BNHA').document('Boku no Hero Academia Chapter ' + str(int(new_chapter))).set(data)
        #var = False
        print("Chapter " + str(int(new_chapter)) + " has been added to the database")
    except Exception as ex:
        print(ex)
