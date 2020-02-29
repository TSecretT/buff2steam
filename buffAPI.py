import requests
from multiprocessing.dummy import Pool as ThreadPool
import json
import time

pool = ThreadPool(8)
GAME = 'dota2'
GAME_ID = '570'
BASE_URL = 'https://buff.163.com'

with open('config.json') as fp:
    config = json.load(fp)

def totalPages():
    j = json.loads(requests.get(BASE_URL+'/api/market/goods',
        params={
        'game': GAME,
        'page_num': 1
        }).content)
    return j['data']['total_page']

def getItemInfo(page_num):
    while True:
        r = requests.get(BASE_URL+'/api/market/goods', headers=headers,
            params={
            'game': GAME,
            'page_num': page_num
            })
        print(page_num, r.status_code)
        try:
            j = json.loads(r.content)
            return j['data']['items']
        except:
            time.sleep(2)
        

def scanItems():
    items=[]
    starttime=time.time()
    total_pages = totalPages()
    results = pool.map(getItemInfo, list(range(1,total_pages+1)))
    for result in results:
        for item in result:
            items.append(item)
    print('Finished in', str(round(time.time()-starttime, 0)), 'seconds.')
    return items



def analyze(item):

market_hash_name = item['market_hash_name']
buff_min_price = float(item['sell_min_price'])
buff_says_steam_price = float(item['goods_info']['steam_price_cny'])

if not config['main']['max_price'] > buff_min_price > config['main']['min_price']:  print('error')
if not buff_says_steam_price:   print('error')
buff_says_ratio = buff_min_price / buff_says_steam_price
if buff_says_ratio > config['main']['accept_buff_threshold']:  print('error')
r = requests.get('https://steamcommunity.com/market/listings/{}/{}/render'.format(GAME_ID, market_hash_name),
    params={
    'count': 1,
    'currency': 23
    })
try:
    j = json.loads(r.content)
except json.decoder.JSONDecodeError: print('json error')
except Exception as e:  print(e)