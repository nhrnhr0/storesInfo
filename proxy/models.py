from urllib import request
from django.db import models
import requests
# Create your models here.
class Proxy(models.Model):
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    isWorking = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ip + ':' + self.port
    
    def use(self, url, headers=None, request_type='get', **kwargs):
        if headers is None:
            headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            }
        proxy = {'https': 'https://' + self.ip + ':' + self.port}
        r = requests.request(request_type,url,proxies=proxy,headers=headers ,timeout=8, **kwargs)
        return r