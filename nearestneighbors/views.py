from django.shortcuts import render

# Create your views here.
import csv,io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import Reviews

@permission_required('admin.can_add_log_entry')
def review_upload (request):
    template="knn_upload.html"

    prompt= {
        'order':'Order of the csv file should be reviews and ratings of the amazon dataset'
    }  #summary clean (reviews) and overall (ratings)

    if request.method == 'GET':
        return render(request,template,prompt)

    csv_file=request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')
    
    data_set=csv_file.read().decode('UTF-8')
    io_string=io.StringIO(data_set)
    next(io_string) #dont wanna upload the header to the database
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Reviews.objects.update_or_create(
            reviews = column[0],
            ratings = column[1]
        )

    context = {}
    return render (request,template,context)