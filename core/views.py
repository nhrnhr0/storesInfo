from django.shortcuts import render
from django.shortcuts import redirect
from core.models import Nearbysearch
from django.contrib import messages

# Create your views here.
def load_nearby_places_file_view(request):
    # redirect to login if not admin
    if not request.user.is_superuser:
        response = redirect('/admin/login/?next=/load_nearby_places/')
        return response
    if request.method == 'POST':
        # get the file
        file = request.FILES['file']
        
        # read csv file
        file_content = file.read().decode('utf-8')
        lines = file_content.split('\n')
        new_count= 0
        full_count = 0
        # headers: X	Y	Name	description
        headers = lines[0].split(',')
        for line in lines[1:]:
            if line:
                fields = line.split(',')
                rad = 2000
                if fields[3]:
                    rad = int(fields[3])
                obj, is_created = Nearbysearch.objects.get_or_create(x=fields[0], y=fields[1], name=fields[2], rad=rad)
                print(obj, is_created)
                if is_created:
                    new_count += 1
                full_count += 1
        
        message = '{} new records added, {} records total'.format(new_count, full_count)
        # redirect to the admin page
        response = redirect('/admin/')
        messages.add_message(request, messages.INFO, message)

        return response
    return render(request, 'load_nearby_places.html')