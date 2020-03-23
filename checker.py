import firebase_admin
from firebase_admin import credentials, firestore
import re

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection("My Hero Academia").stream()
listnum = []
b = "''[]"

for doc in docs:
    name = doc.id

    #find all numbers and convert to str
    num = re.findall(r'[\d\.\d]+', name)
    num = str(num)
    
    #remove ''[] char in num
    for char in b:
        num = num.replace(char,"")
    num = float(num)
    listnum.append(num)

listnum.sort()
print(listnum)
