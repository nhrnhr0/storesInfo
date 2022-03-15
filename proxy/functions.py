
from .models import Proxy

def get_working_proxy():
    working_proxy = Proxy.objects.filter(isWorking=True)
    if working_proxy.count() > 0:
        return working_proxy.order_by('?').first()
    else:
        Proxy.objects.all().order_by('?').first()
        
def send_with_random_proxy(url, headers=None, request_type='get', **kwargs):
    while True:
        try:
            proxy = get_working_proxy()
            print('Using Proxy {}'.format(proxy))
            response = proxy.use(url, headers, request_type, **kwargs)
            return response
        except Exception as e:
            proxy.isWorking = False
            proxy.save()
            #print(e)
            print('Proxy {} is not working'.format(proxy))
            continue