import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/home/ansuman/scrape/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection("Haikyuu").stream()
flag = False

for doc in docs:
    dicct = doc.to_dict()
    img_list = dicct['images']
    num = dicct['number']
    
    n = str(num)
    if n[-1] == '0':
        num = int(num)

    #remove 'text' from the image links
    for i in range(len(img_list)):
        link = img_list[i]
        for j in range(len(link)-6):
            if link[j] == 'l' and link[j+1] == '=' and link[j+2] == 'h' and link[j+3] == 't' and link[j+4] == 't':
                sliced_string = link[j+2:len(link)]

                img_list[i] = sliced_string
                flag = True
    
    if flag:
        data = {
            'images': img_list,
            'number': num
        }
    
        db.collection('Haikyuu').document('Haikyuu Chapter ' + str(num)).set(data)
        print("Fixed chapter " + str(num))
    flag = False
