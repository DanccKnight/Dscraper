import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
import time

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

web_url = 'https://ww5.readmha.com/manga/boku-no-hero-academia/'

r = requests.get(web_url)
soup = BeautifulSoup(r.text,'html.parser')
links_set = soup.find_all('a', class_ = "text-gray-900 dark:text-white text-lg font-semibold mb-1")

chapter_links = []
chapter_text = []

for link in links_set:
    chapter_links.append(str(link['href']))
    chapter_text.append(link.text)

for link in chapter_links:
    try:
        image_links = []
        web_url = link
        r = requests.get(web_url)
        soup = BeautifulSoup(r.text,'html.parser')
        img_set = soup.find_all('img', class_ = "my-3 mx-auto js-page")
    
        for x in img_set:
            content = str(x['src'])
            if(content[len(content)-1] == '0'):
                continue
            image_links.append(str(x['src']))
   
        if (len(image_links) < 3):
            continue
        index = chapter_links.index(link)
        print("Chapter Name:- " + chapter_text[index])
        print("Chapter link:- " + link)
        print("Number of image links fetched:" + str(len(image_links)))
        print("Image links:-")   
        
        for x in image_links:
            print(x)
        print("")
        
        data = {
            u'images': image_links   
        }
    
        db.collection(u'My Hero Academia').document(chapter_text[index]).set(data)
        print("Suspending for 3 seconds...")
        time.sleep(3)
    except:
        print("Something went wrong :(")

print("Uploaded all chapters successfully!")
