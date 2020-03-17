from django.shortcuts import render

# Create your views here.
<<<<<<< HEAD


=======
<<<<<<< HEAD
from django.http import HttpResponse


from django.http import JsonResponse
from polls.models import Order
from django.core import serializers

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})

def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
=======
>>>>>>> 7a50073983964f4409d06656e77d26698325ec5d
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")
>>>>>>> 1a407a20157accad21830d32f020762c66cef39e
