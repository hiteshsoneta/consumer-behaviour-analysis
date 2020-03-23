from django.core import serializers
from polls.models import Order
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")


def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})


def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")
