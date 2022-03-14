from .secrects import GMA_KEY
import requests

def gma_search_nearby(x, y, rad, page_token=None):
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    LOCATION_URL =  str(y)  + ',' + str(x) + '&radius=' + str(rad) + GMA_KEY
    if page_token:
        LOCATION_URL += '&pagetoken=' + page_token
    req_url = BASE_URL + LOCATION_URL
    req_url = req_url.replace(' ', '%20')
    reponse = requests.get(req_url)
    data = reponse.json()
    print('request: ', req_url)
    return data


def gma_get_place_detail(place_id):
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='
    PLACE_URL = place_id + GMA_KEY
    req_url = BASE_URL + PLACE_URL
    req_url = req_url.replace(' ', '%20')
    reponse = requests.get(req_url)
    print('request: ', req_url)
    data = reponse.json()
    return data