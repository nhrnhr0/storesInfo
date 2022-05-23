from bs4 import BeautifulSoup
from django.contrib import admin
from django.http import HttpResponse
from .models import Nearbysearch, Place, EasyList, EasyPage, EasyCategory
from advanced_filters.admin import AdminAdvancedFiltersMixin
import csv
# Register your models here.
class NearbysearchAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('name', 'x', 'y', 'rad', 'loaded')
    actions = ['load_nearby_places']
    advanced_filter_fields = ('name', 'x', 'y', 'rad')
    
    def load_nearby_places(self, request, queryset):
        for nearbysearch in queryset:
            nearbysearch.load_nearby_places()
admin.site.register(Nearbysearch, NearbysearchAdmin)

class PlaceAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    search_fields = ['name', 'address', 'nearbysearch__name', 'types', 'detailResponse' ]
    list_display = ('name','isBusiness', 'address','formated_phone', 'nearbysearch', 'types')
    list_editable = ('isBusiness',)
    list_filter = ('nearbysearch',)
    actions = ('export_business_to_csv', 'export_all_to_csv')
    def export_business_to_csv(self, request, queryset):
        queryset = queryset.filter(isBusiness=True)
        return self.export_to_csv(request, queryset)
    def export_all_to_csv(self, request, queryset):
        return self.export_to_csv(request, queryset)
    def export_to_csv(self, request, queryset):
        response = HttpResponse(
        content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['name', 'address', 'phone','Place id', 'x', 'y', 'url'])
        for place in queryset:
            if place.formated_phone:
                writer.writerow([place.name, place.address, place.formated_phone, place.place_id, place.x, place.y, place.url])
        return response
        
    advanced_filter_fields = ('detailResponse','name','address','rating','place_id','types','vicinity','x','y','nearbysearch','businessStatus','permenentlyClose','userRatingTotal','formated_phone','internal_phone','url','createdAt','updatedAt','website','addressComponents')
admin.site.register(Place, PlaceAdmin)

class EasyPageAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    search_fields = ['name', 'url']
    list_display = ('id', 'name', 'page_id', 'hasData', 'url',)
    advanced_filter_fields = ('name', 'url')
    actions = ('load_page_data_to_empty_places','download_to_csv')
    def load_page_data_to_empty_places(self, request, queryset):
        for page in queryset:
            if page.hasData == False:
                page.easy_data_request()
    def download_to_csv(self, request, queryset):
        response = HttpResponse(
        content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['name', 'url', 'page_id', 'phone', 'lat', 'lng',])
        for page in queryset:
            if page.hasData and page.html:
                bs = BeautifulSoup(page.html, 'html.parser')
                #phone = bs.find('#action-side-2-label')
                #addr = bs.find('.biz-address-text')
                #if addr:
                    #addr = addr.text
                writer.writerow([page.name, page.url, page.page_id, page.phone, page.lat, page.lng])
        return response
admin.site.register(EasyPage, EasyPageAdmin)

class EasyListAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    actions = ('load_list',)
    search_fields = ['name',]
    list_display = ('name', )
    filter_horizontal = ('categories','pages')
    advanced_filter_fields = ('name',)
    
    def load_list(self, request, queryset):
        for easylist in queryset:
            easylist.load_list()
admin.site.register(EasyList, EasyListAdmin)

class EasyCategoryAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    search_fields = ['name','url', 'c']
    list_display = ('id', 'name', 'url', 'c')
    advanced_filter_fields = ('name','url', 'c')
admin.site.register(EasyCategory, EasyCategoryAdmin)