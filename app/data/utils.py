
from app.extensions import mongo
from requests import get
from json import loads
from json.decoder import JSONDecodeError  
from bs4 import BeautifulSoup               
import os
import time #TODO: remove in prod
import math #TODO: remove in prod

def extract_data():
    
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

def scrape_indiatoday():
    res = []
    l = "https://www.indiatoday.in/coronavirus-covid-19-outbreak"
    data = get(l)
    soup = BeautifulSoup(data.content, "lxml")
    news_divs = soup.find_all("div", {"class": "catagory-listing"})
    for news in news_divs:
        title = news.h2.text.strip()
        alink = news.a
        if news.img:
            img = news.img
            img = img.get('src')
            img = img.replace('170x96', '647x363')
        else:
            img = ''
        try:
            res.append({'title': title, 'link': 'https://www.indiatoday.in'+alink.get('href'),'img': img})
        except:
            continue
    return res

def scrape_ABP():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    resp = get('https://news.abplive.com/search?s=coronavirus', headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    news = soup.findAll('a', {'class': 'news_featured'})

    res = []
    for article in news:
        img_src = article.find('img')['src']
        title = article.find(
            'div', {'class': 'news_content'}).findChild('p').text.strip()
        link = article['href']
        if 'Deaf And Abled People' not in title:
            res.append({
                'title': title,
                'img': img_src,
                'link': link
            })
    return res

def scrape_NN():
    res = []
    headers = headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
            }
    resp = get('https://www.newsnation.in/topic/coronavirus-news', headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    news = soup.findAll('div', {'class': 'col-xs-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 mt-2'})
    # col-xs-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 mt-2
    for article in news:
        article_container = article.findChild('a')
        relative_link = article_container['href']
        link = f"https://www.newsnation.in{ relative_link }"
        img_src = article_container.findChild('div', {'class': 'position-relative'}).findChild('img')['src']
        title = article_container.findChild('h3').text.strip()
        res.append({
            'title': title,
            'link' : link,
            'img'  : img_src
        })

    return res

def scrape_ani():
    res = []
    anilink = 'https://www.aninews.in/topic/coronavirus/'
    ani = get(anilink)
    soup = BeautifulSoup(ani.content, 'html.parser')
    anidiv = soup.find_all('div', class_='card')
    for b in anidiv:
        if(b.img):
            aniimg = b.img
            aniimg = aniimg.get('data-src')
            aniimg = aniimg.replace('/__sized__/', '/')
            aniimg = aniimg.replace('-thumbnail-320x180-70.', '.')
        else:
            aniimg = ''
        title = b.h6
        try:
            title = title.text
        except:
            continue
        aani = b.a
        try:
            aani = aani.get('href')
            aani = 'https://www.aninews.in'+aani
        except:
            continue
        res.append({'title': title, 'link': aani, 'img': aniimg})
    return res


def scrape_news():
    
    res = scrape_indiatoday()
    res.extend(scrape_ani())
    res.extend(scrape_ABP())
    res.extend(scrape_NN())
    print('News scraped')

    return res

def extract_and_import_db():

    s = time.time() # to measure how long this takes.

    entries = extract_data() # get data from Google Sheet
    delete_data_db() # Delete existing data
    entries_collection = mongo.db.entries
    entries_collection.insert_many(entries)
    print("Data added!")

    news = scrape_news()
    delete_news_db() # Delete existing news
    news_collection = mongo.db.news
    news_collection.insert_many(news)
    print('News added!')

    end = time.time()
    print(f'Time taken {math.floor((end-s))}secs') # remove this in prod.

def delete_data_db():

    print("Deleting data before adding ...")

    data = mongo.db.entries
    data.delete_many({})

def delete_news_db():

    print("Deleting news before adding..")

    news = mongo.db.news
    news.delete_many({})

if __name__ == '__main__':
    s = time.time()
    extract_and_import_db()
    print(time.time()-s)
