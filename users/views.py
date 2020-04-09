from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, prodidForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import City
from .models import Country
from django.shortcuts import render
import csv
import io
# from .data_provider import get_data
import pickle
from django.db.models import Sum
from django.http import JsonResponse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from consumerbehaviour import settings
import os
# Create your views here.
from django.conf.urls.static import static

import shutil
from django.urls import reverse

# Create your views here.



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # img = form.cleaned_data.get("image")
            # obj = Profile.objects.create(
            #     image=img
            # )
            # obj.save()
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            #messages.success(request, f'Your Account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form

    }
    return render(request, 'users/profile.html', context)

@login_required
def country(request):
    template = 'country.html'
    if request.method == "GET":
        return render(request, template)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(
            request, 'not a csv file,please enter a csv file to continue..')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        created = Country.objects.update_or_create(
            name=column[0],
        )
    context = {}
    return render(request, template, context)


@login_required
def city(request):
    template = 'city.html'
    if request.method == "GET":
        return render(request, template)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):

        messages.error(
            request, 'not a csv file,please enter a csv file to continue..')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        created = City.objects.update_or_create(
            name=column[0],
            country=column[1],
            population=column[2],
        )
    context = {}
    return render(request, template, context)


def pie_chart(request):

    data = dict()
    file = open('C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file', 'rb')
    dat = pickle.load(file)

    for key in dat.keys():
        data.update({
            key: dat[key]
        })

    file.close()

    # queryset = City.objects.order_by('-population')[:5]
    # for city in queryset:
    #     labels.append(city.name)
    #     data.append(city.population)

    return render(request, 'users/pie_chart.html', {
        'labels': list(data.keys())[:50],
        'data': list(data.values())[:50],
    })


def home(request):

    return render(request, 'users/home.html')


def population_chart(request):

    data = dict()
    file = open('C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file', 'rb')
    dat = pickle.load(file)

    for key in dat.keys():
        data.update({
            key: dat[key]
        })

    file.close()

    labels = list(data.keys())[:10]
    data = list(map(lambda x: int(x), list(data.values())[:10]))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def countrating1(request):
    return render(request, 'users/countrating1.html')


def countrating(request):

    data = dict()
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file1', 'rb')
    dat = pickle.load(file)

    for key in dat.keys():
        data.update({
            key: dat[key]
        })

    file.close()

    labels = list(map(lambda x: int(x), list(data.keys())))
    data = list(map(lambda x: int(x), list(data.values())))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def countrating2(request):
    return render(request, 'users/countrating2.html')


def cntrating(request):

    data = dict()
    file = open('C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file2', 'rb')
    dat = pickle.load(file)

    for key in dat.keys():
        data.update({
            key: dat[key]
        })

    file.close()

    labels = list(data.keys())
    data = list(map(lambda x: int(x), list(data.values())))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def distprod(request, prod_id):
    # data = dict()
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file3', 'rb')
    dat = pickle.load(file)

    df_1prod = dat[dat['asin'] == prod_id]['overall']
    df_1prod_plot = df_1prod.value_counts(sort=False)
    ax = df_1prod_plot.plot(kind='bar', figsize=(15, 10), title='Rating distribution of Product {} review'.format(
        dat[dat['asin'] == prod_id]['asin'].iloc[0]))
    plt.savefig(os.path.join(settings.BASE_DIR, "media", prod_id + ".png"))

    file.close()

    return render(request, 'users/distprod.html', {
        'img_src': settings.MEDIA_URL + "/{}.png".format(prod_id)
    })


def distcust(request, cust_id):
    # DELETE ALL THE FILES IN THE MEDIA_ROOT FOLDER
    # user_id = "A1IU7S4HCK1XK0"
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file4', 'rb')
    dat = pickle.load(file)

    df_1user = dat[dat['reviewerID'] == cust_id]['overall']
    df_1user_plot = df_1user.value_counts(sort=False)
    ax = df_1user_plot.plot(kind='bar', figsize=(15, 10), title='Rating distribution of user {} review'.format(
        dat[dat['reviewerID'] == cust_id]['reviewerID'].iloc[0]))

    plt.savefig(os.path.join(settings.BASE_DIR, "media", cust_id + ".png"))

    file.close()

    return render(request, 'users/distcust.html', {
        'img_src': settings.MEDIA_URL + "/{}.png".format(cust_id)
    })

def enterprodid(request):
    if request.method == 'POST':
        form = prodidForm(request.POST)

        if form.is_valid():
            prod_id = form.cleaned_data.get('prodid')

            # return render(request, 'users/distprod.html', {'img_src': reverse('distprod', kwargs={'prod_id': prod_id})})
            return redirect('distprod', prod_id)
    else:
        form = prodidForm()
    return render(request, 'users/prodid.html', {'form': form})


def enteruserid(request):

    if request.method == 'POST':
        form = prodidForm(request.POST)
        if form.is_valid():
            prod_id = form.cleaned_data.get('prodid')

            # return render(request, 'users/distprod.html', {'img_src': reverse('distprod', kwargs={'prod_id': prod_id})})
            return redirect('distcust', prod_id)
    else:
        form = prodidForm()

    return render(request, 'users/cust.html', {'form': form})



