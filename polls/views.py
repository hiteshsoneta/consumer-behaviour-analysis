from django.core import serializers
from polls.models import Order
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
<<<<<<< HEAD


=======
<<<<<<< HEAD
=======
<<<<<<< HEAD


=======
<<<<<<< HEAD
>>>>>>> c2f137ec8001eace770b681e2aa440b4e5402b73
from django.http import HttpResponse


from django.http import JsonResponse
from polls.models import Order
from django.core import serializers

>>>>>>> b28fdefeef87774bc89a219bc220cbfea60fe13f
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")


def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})


def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
<<<<<<< HEAD


=======
<<<<<<< HEAD

=======
=======
>>>>>>> 7a50073983964f4409d06656e77d26698325ec5d
>>>>>>> c2f137ec8001eace770b681e2aa440b4e5402b73
>>>>>>> b28fdefeef87774bc89a219bc220cbfea60fe13f
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "index.html")
