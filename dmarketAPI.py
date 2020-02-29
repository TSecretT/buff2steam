import requests
from multiprocessing.dummy import Pool as ThreadPool
import json
import time
pool=ThreadPool(8)
username='timichfull@gmail.com'
password='Lordelover29'

headers = {
    'authorization': None
}

def login(username, password, captcha=''):
    s = requests.Session()
    r = requests.post('https://api.dmarket.com/marketplace-api/v1/sign-in',
        json={
        "Email": username,
        "Password": password,
        })
    try:
        if json.loads(r.content)['Result'] == 'Authorized':
            headers['authorization'] = json.loads(r.content)['AuthToken']
            return s
        return r.content
    except:
        return r.content


def loadItems(order_by='best_discount', limit=100):
    if limit > 100:
        print('Max limit: 100')
        return
    r = requests.get('https://api.dmarket.com/exchange/v1/market/items',
        params={
        'orderBy': order_by,
        'gameId': '9a92',
        'limit': limit,
        'currency': 'USD'
        })
    try:
        return json.loads(r.content)
    except:
        return r.content

def loadUserItems(limit=100):
    if limit > 100:
        print('Max limit: 100')
        return
    if not headers['authorization']:
        print('Login required')
        return
    r = s.get('https://api.dmarket.com/exchange/v1/user/items', headers=headers,
        params={
        'orderBy': 'updated',
        'gameId': '9a92',
        'limit': limit,
        'currency': 'USD'
        })
    try:
        j = json.loads(r.content)
    except:
        return r.content
    total_items = j['total']['items']
    user_items=[]
    for i in range(0, int(total_items/limit)+1):
        offset = limit*(i)
        j = json.loads(s.get('https://api.dmarket.com/exchange/v1/user/items', headers=headers,
        params={
        'orderBy': 'updated',
        'gameId': '9a92',
        'limit': limit,
        'currency': 'USD',
        'offset': offset
        }).content)
        for item in j['objects']:
            user_items.append(item)
    return user_items