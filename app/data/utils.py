
from app.extensions import mongo
from dotenv import load_dotenv
from requests import get
from json import loads
from json.decoder import JSONDecodeError                 
import os
import time #TODO: remove in prod
import math #TODO: remove in prod

def extract_data():
    #sheet_id = '10q6rF4JuSz-gPq82MNWfzz7Bm_zOnZDFUtx9XM63f9I' #Test sheet id.
    load_dotenv()
    SHEET_ID = os.getenv('G_SHEET_ID', None)

    if SHEET_ID is None:
        print("Please add the Sheet ID to .env file!")
        return

    sheet_id = SHEET_ID #Main google sheet id.
    tab_num = 1 # tabs represent categories.
    
    # By default in Google sheet, we don't want to include them.
    exclude = {'Access', 'Not Used', 'Formula'} 
    
    # `all_entries` will be populatd below.
    all_entries = []
    
    while True:
        
        #this URL returns the sheet data in JSON for that particular tab.
        sheet_url = f'https://spreadsheets.google.com/feeds/list/{sheet_id}/{tab_num}/public/full?alt=json'
        print(f"Extracting tab_num {tab_num}..")
        resp = get(sheet_url)
        
        # to check if the tab exists or not.
        if resp.status_code is not 200:
            break

        #in case sheet isn't published, we won't be sent an error status code but a custom response that is not json, so this will accommodate those cases.
        try:
            j = resp.json()
        except JSONDecodeError:
            break
        
        #title of the tab represents category.
        category_tab = j['feed']['title']['$t']
        if category_tab not in exclude:


            entries = j['feed']['entry']
            entries_keys = j['feed']['entry'][0].keys()
            #only the fields that are prefixed by 'gsx$' are the ones that we want, filter the rest.
            entries_keys = tuple(filter(lambda x: 'gsx$' in x, entries_keys))
            
            #these are the corresponding keys that we'll store in our data.
            data_keys = { k: k.split('$')[1] for k in entries_keys}  # eg: gsx$phone_1 -> phone_1
            
            for entry in entries:
                #dict comprehension to get the data we want, in the right format.
                obj = { data_keys[k]: entry[k]['$t'] for k in entries_keys}
                all_entries.append(obj)
        tab_num+=1
    
    print("Extracted all data")

    return all_entries

def extract_and_import_db():
    s = time.time() # to measure how long this takes.
    entries = extract_data() # gets all the entries from Google Sheet
    print("Deleting entries before adding ...")
    delete_entries_db() # delete existing entries
    entries_collection = mongo.db.entries
    entries_collection.insert_many(entries)
    end = time.time()
    print("Entries added!")
    print(f'Time taken {math.floor((end-s))}secs') # remove this in prod.

def delete_entries_db():
    entries = mongo.db.entries
    entries.delete_many({})

if __name__ == '__main__':
    s = time.time()
    extract_and_import_db()
    print(time.time()-s)
