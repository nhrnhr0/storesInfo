from decimal import Decimal
import json
from django.db import models
from proxy.functions import send_with_random_proxy
from Locs.utils import gma_get_place_detail
from bs4 import BeautifulSoup
import requests
from Locs.utils import gma_search_nearby
from playwright.sync_api import sync_playwright
import time
class Place(models.Model):
    isBusiness = models.BooleanField(default=False)
    detailResponse = models.JSONField(blank=True, null=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rating = models.FloatField(blank=True, null=True)
    place_id = models.CharField(max_length=200, unique=True)
    types = models.CharField(max_length=200, blank=True, null=True)
    vicinity = models.CharField(max_length=200, blank=True, null=True)
    x = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    y = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    nearbysearch = models.ForeignKey(to='Nearbysearch', on_delete=models.SET_NULL, null=True)
    businessStatus = models.CharField(max_length=200, blank=True, null=True)
    permenentlyClose = models.BooleanField(default=False)
    userRatingTotal = models.IntegerField(blank=True, null=True)
    formated_phone = models.CharField(max_length=200, blank=True, null=True)
    internal_phone = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    addressComponents = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
# Create your models here.
class Nearbysearch(models.Model):
    x = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    y = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    rad = models.IntegerField(blank=True, null=True, default=2000)
    loaded = models.BooleanField(default=False)
    class Meta:
        unique_together = ('x', 'y', 'name', 'rad')
    def __str__(self):
        return self.name + ' ' + str(self.rad)
    
    def nearby_results_to_places(self, results):
        from core.models import Place
        for result in results:
                x = result['geometry']['location']['lat']
                y = result['geometry']['location']['lng']
                name = result['name']
                place_id = result['place_id']
                types = str(result['types'])
                vicinity = result.get('vicinity', '')
                businessStatus = result.get('business_status', None)
                rating = result.get('rating', None)
                totalRating = result.get('user_ratings_total', None)
                place, is_created = Place.objects.get_or_create(place_id=place_id)
                if is_created:
                    details = gma_get_place_detail(place_id).get('result', None)
                    international_phone_number = details.get('international_phone_number', None)
                    formatted_phone_number = details.get('formatted_phone_number', None)
                    formatted_address = details.get('formatted_address', None)
                    address_components = json.dumps(details.get('address_components', None))
                    url = details.get('url', None)
                    website = details.get('website', None)
                    permenentlyClose = details.get('permanently_closed', False)
                    place.x = x
                    place.y = y
                    place.detailResponse = details
                    place.name = name
                    place.types = types
                    place.vicinity = vicinity
                    place.businessStatus = businessStatus
                    place.rating = rating
                    place.userRatingTotal = totalRating
                    place.formated_phone = formatted_phone_number
                    place.internal_phone = international_phone_number
                    place.url = url
                    place.website = website
                    place.addressComponents = address_components
                    place.permenentlyClose = permenentlyClose
                    place.nearbysearch = self
                    place.address = formatted_address
                    '''
                    place, is_created = Place.objects.get_or_create(x=x, y=y,detailResponse=details, name=name, place_id=place_id, types=types, vicinity=vicinity,  \
                                businessStatus=businessStatus, rating=rating, userRatingTotal=totalRating, \
                                formated_phone=formatted_phone_number, internal_phone=international_phone_number, \
                                url=url, website=website, addressComponents=address_components, \
                                permenentlyClose=permenentlyClose, nearbysearch=self, address=formatted_address)
                    '''
                    print(place, is_created)
                    place.save()
                
    
    def load_nearby_places(self, nextpage_token=None):
        
        response = gma_search_nearby(self.x, self.y, self.rad, nextpage_token)
        
        if 'results' in response:
            results = response['results']
            self.nearby_results_to_places(results)
        if 'next_page_token' in response:
            nextpage_token = response['next_page_token']
            self.load_nearby_places(nextpage_token)
        self.loaded = True
        

class EasyCategory(models.Model):
    url = models.CharField(max_length=200, blank=True, null=True, unique=True)
    c = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    def __str__(self):
        return self.name
class EasyPage(models.Model):
    name = models.CharField(max_length=200)
    page_id = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    bestsubcat = models.CharField(max_length=200, blank=True, null=True)
    logo = models.CharField(max_length=200, blank=True, null=True)
    infoBox = models.TextField(blank=True, null=True)
    hasData = models.BooleanField(default=False)
    html = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
    def easy_data_request(self):
        if self.url is not None and self.url != '':
            url = self.url
        else:
            url = 'https://easy.co.il/page/' + self.page_id
        response = requests.get(url) #send_with_random_proxy(url)
        time.sleep(2.3)
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')
            self.html = soup.prettify()
            self.name = soup.find('h1', {'class':'biz-title'}).text
            phoneEl = soup.find('span', {'id': 'action-phone-label'})
            if phoneEl:
                self.phone = phoneEl.text
                
            
            addressEl = soup.find('span', {'class': 'biz-address-text'})
            if addressEl:
                self.address = addressEl.text.replace('\n', '').strip()
            
            logoEl = soup.find('div', {'class': 'biz-logo'})
            if logoEl:
                self.logo = logoEl.find('img')['src']
            mapEl = soup.find('div', {'class': 'map-image'})
            if mapEl:
                staticmap_src = mapEl.find('img')['src'] # https://easy.co.il/n/getStaticMapByCoord?lat=32.075987&lng=34.902733&lang=he&zoom=13
                # extract lat and lng from staticmap_src
                lat = staticmap_src.split('lat=')[1].split('&')[0]
                lng = staticmap_src.split('lng=')[1].split('&')[0]
                self.lat = Decimal(lat)
                self.lng = Decimal(lng)
            self.url = url
            infoBoxEl = soup.find('div', {'class': 'info-box'})
            if infoBoxEl:
                self.infoBox = infoBoxEl.prettify()
            self.hasData = True
            #self.hasData = True
            self.save()
            print(self.name, self.phone, self.address, self.logo)

# c: 234 | https://easy.co.il/list/Carpenters | נגרים ונגריות
# c: 4935 | https://easy.co.il/list/Garages | מוסכים
# c: 17461 | https://easy.co.il/list/Professionals | בעלי מקצוע
# c: 33 | https://easy.co.il/list/Business-Services | שירותים לעסק
# c: 5283 | https://easy.co.il/list/Animal-Care | טיפול בבעלי חיים
# c: 20218 | https://easy.co.il/list/Help-&-Services | שירותים ועזרה
# c: 15863 | https://easy.co.il/list/Agriculture-Nature-and-Environment | חקלאות טבע וסביבה
# c: 131 | https://easy.co.il/list/Restaurants-and-Fast-Food | מסעדות ומזון מהיר
# c: 26117 | https://easy.co.il/list/easyfix | easyfix
# c: 252 | https://easy.co.il/list/Plumbers | אינסטלטורים
# c: 235 | https://easy.co.il/list/Locksmiths | מנעולנים
# c: 222 | https://easy.co.il/list/Electricians | חשמלאים
# c: 204 | https://easy.co.il/list/Boilers-Technicians | טכנאי דודים
# c: 2853 | https://easy.co.il/list/Air-Conditioner-Technicians | טכנאי מזגנים
# c: 2927 | https://easy.co.il/list/Glaziers | זגגים
# c: 21105 | https://easy.co.il/list/Computer-Technicians | טכנאי מחשבים
# c: 5421 | https://easy.co.il/list/Handyman | הנדימן
# c: 248 | https://easy.co.il/list/Renovations | שיפוצניקים
# c: 26777 | https://easy.co.il/list/Mobile-Cellular-Labs | מעבדות סלולר ניידות
# c: 211 | https://easy.co.il/list/Pest-Control | מדבירים
# c: 424 | https://easy.co.il/list/Bars-and-Pubs | בארים ופאבים
# c: 12952 | https://easy.co.il/list/Events-for-children | אירועים לילדים
class EasyList(models.Model):
    isLoaded = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    rad = models.IntegerField(default=2000)
    categories = models.ManyToManyField(to='EasyCategory', blank=True)
    pages = models.ManyToManyField(to='EasyPage', blank=True)
    # Using Proxy {'https': '190.90.83.225:999'}
    
    def __str__(self):
        return self.name
    # lang: he
    def load_list(self):
        request_type = "get"
        #requests.get()
            # center: 30.87438, 34.79305
            # example: https://easy.co.il/json/list.json?v=1.2&c=17755&listpage=1&lat=0&lng=0&rad=212478
            # example: https://easy.co.il/json/list.json?v=1.2&c=17755&listpage=1&lat=30.87438&lng=34.79305&rad=21247
        for category in self.categories.all():
            hasNext = True
            i = 1
            pages = []
            #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            url = 'https://easy.co.il/json/list.json?v=1.2&c=' + category.c + '&listpage=1&lat=' + str(self.lat) + '&lng=' + str(self.lng) + '&rad=' + str(self.rad)
            #response = requests.get(url,headers=headers)
            #response = proxy.Proxy_Request(url=url, request_type=request_type)
            response = send_with_random_proxy(url=url, request_type=request_type)
            data = response.json()
            if data.get('error'):
                print('ERROR ==> ', url)
                continue
            time.sleep(2.3)
            #category = data['bizlist']['catparams'] # "c=21105"
            allbizim = data['bizlist']['allbizim']
            places = allbizim.split('|')
            for p in places:
                if p == '':
                    continue
                obj, created = EasyPage.objects.get_or_create(page_id = p)
                #print(created, obj)
            #size = str(len(places))
            
            #print('name:', self.name, ' | category: ' + str(category) + ' | size: ' + size)
            bis_list = data['bizlist']['list']
            for bis in bis_list:
                name = bis.get('bizname')
                page_id = bis.get('id')
                url = 'https://easy.co.il' + bis.get('url')
                lat = bis.get('lat')
                lng = bis.get('lng')
                phone = bis.get('phone')
                address = bis.get('address')
                bestsubcat = bis.get('bestsubcat')
                logo = bis.get('logo')
                obj, created = EasyPage.objects.get_or_create(page_id=page_id)
                obj.name=name
                obj.url=url
                obj.lat=lat
                obj.lng=lng
                obj.phone=phone
                obj.address=address
                obj.bestsubcat=bestsubcat
                obj.logo=logo
                obj.hasData = True
                obj.save()
                #print(created, page_id, name)
                pages.append(obj)
                pass # end of this page bis list
            pass # end of this category list
            print('loaded:', self.name, ' | category: ' + str(category) + ' | pages: ' + str(len(pages)))
            self.pages.add(*pages)
            self.save()
        self.save()