from django.contrib import admin
from .models import Proxy
import requests
from bs4 import BeautifulSoup

# Register your models here.
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('ip', 'port', 'isWorking', 'last_checked')
    list_filter = ('isWorking',)
    search_fields = ('ip', 'port')
    ordering = ('-last_checked',)
    actions = ('load_proxies',)
    def load_proxies(self, request, queryset):
        __url = 'https://www.sslproxies.org/'
        __headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            }
        r = requests.get(url=__url, headers=__headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        random_port = []
        random_ip = []
        # Get the Random IP Address
        for x in soup.findAll('td')[::8]:
            random_ip.append(x.get_text())

        # Get Their Port
        for y in soup.findAll('td')[1::8]:
            random_port.append(y.get_text())

        # Zip together
        z = list(zip(random_ip, random_port))
        
        for ip,port in z:
            proxy = Proxy.objects.create(ip=ip, port=port)
            proxy.save()
admin.site.register(Proxy, ProxyAdmin)