import json
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials, firestore
from googleapiclient.discovery import build

f = open('googleapikey.json')
json_data = json.load(f)
api_key = json_data['api_key']
cx = json_data['cx']

# https://github.com/googleapis/google-api-python-client/blob/main/samples/customsearch/main.py
def custom_search(search_term, api_key, cse_id, index):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType="image", num=index).execute()
    url = []
    for item in res['items']:
        url.append(item["link"])
    return url

def listener(event):
    if event.event_type == 'put':
        print("new data added")
        keyword = event.data
        urls = custom_search(f'{keyword}', api_key, cx, 10)
        ref = firebase_admin.db.reference('image_link')
        ref.set(urls)

if __name__ == '__main__':

    # connect to database
    cred = credentials.Certificate("myscorecard-6388b-firebase-adminsdk-o5dnl-b7fde33bd0.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://myscorecard-6388b-default-rtdb.firebaseio.com/'
    })

    firebase_admin.db.reference('keyword').listen(listener)

