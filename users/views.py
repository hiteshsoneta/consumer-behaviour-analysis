from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, prodidForm
from django.contrib.auth.decorators import login_required, permission_required
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
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from consumerbehaviour import settings
import os
# Create your views here.
from django.conf.urls.static import static
import seaborn as sns
import shutil
from django.urls import reverse
import regex as re
from wordcloud import WordCloud, STOPWORDS

import threading

@login_required
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


@login_required
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
            messages.success(request, f'Your Account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form

    }
    return render(request, 'users/profile.html', context)




def pie_chart(prod_id):

    
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\bingo', 'rb')
    data = pickle.load(file)
    rating_perperson = data.reviewerID.value_counts()
    rating_perperson.value_counts().plot(
        kind='pie', figsize=(10, 10), title='Ratings Per User')
    plt.savefig(os.path.join(settings.BASE_DIR, "media", prod_id + ".png"))
    file.close()



def home(request):

    return render(request, 'users/home.html')


def population_chart(request):

    data = dict()
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\users\\static\\users\\file', 'rb')
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


def heatmap(prod_id):
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\bingo', 'rb')
    reviews = pickle.load(file)
    df_s = reviews.groupby(['overall', '% Upvote']).agg({'Id': 'count'})
    df_s = df_s.unstack()
    df_s.columns = df_s.columns.get_level_values(1)
    fig = plt.figure(figsize=(15,10))

    sns.heatmap(df_s[df_s.columns[::-1]].T, cmap = 'YlGnBu', linewidths=.5, annot = True, fmt = 'd', cbar_kws={'label': '# reviews'})
    plt.yticks(rotation=0)
    plt.title('How helpful users find among the user scores')

    plt.savefig(os.path.join(settings.BASE_DIR, "media", prod_id + ".png"))

    file.close()




def countrating1(prod_id):
    #prod_id = 'abcdfghij'
    # file = open(
    #     'C:\\Users\\Hitesh\\Documents\\BE\\Consumer-Behaviour-Analysis\\users\\static\\users\\check', 'rb')
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\bingo', 'rb')
    data = pickle.load(file)
    review=pd.DataFrame(data.groupby('overall').size().sort_values(ascending=False).rename('No of Users').reset_index())
    plt.figure(figsize=(10, 5))
    sns.countplot(data['overall'])
    plt.title('Count ratings')
    

    plt.savefig(os.path.join(settings.BASE_DIR, "media", prod_id + ".png"))

    file.close()

    


def countrating2(prod_id):

    #prod_id = 'abcde'
    # file = open(
    #     'C:\\Users\\Hitesh\\Documents\\BE\\Consumer-Behaviour-Analysis\\users\\static\\users\\check', 'rb')
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\bingo', 'rb')
    data = pickle.load(file)
    plt.figure(figsize=(10, 5))
    sns.countplot(data['% Upvote'])
    plt.title('Count Helpful %')

    plt.savefig(os.path.join(settings.BASE_DIR, "media", prod_id + ".png"))

    file.close()

   


@login_required
def distprod(request, prod_id):
    file = open('C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\bingo', 'rb')
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

@login_required
def distcust(request, cust_id):
   
    file = open(
        'C:\\Users\\juyee\\Envs\\beproject1\\consumer-behaviour-analysis\\bingo', 'rb')
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

@login_required
def create_image(request):
    p1 = 'abc'
    p2 = 'abcd'
    p3 = 'abcde'
    p5='heatmapimg'
    pie_chart(p1)
    countrating1(p2)
    countrating2(p3)
    heatmap(p5)
    return render(request, 'users/createimage.html', {
        'img_src1': settings.MEDIA_URL + "/{}.png".format(p1),
        'img_src2': settings.MEDIA_URL + "/{}.png".format(p2),
        'img_src3': settings.MEDIA_URL + "/{}.png".format(p3),
        'img_src4': settings.MEDIA_URL + "/{}.png".format(p5),

    })


@login_required
def dataset_upload(request):
    template = "users/upload.html"

    prompt = {
        'order': 'Upload the dataset'
    }  # summary clean (reviews) and overall (ratings)

    if request.method == 'GET':
        return render(request, template, prompt)

    json_file = request.FILES['file']

    if not json_file.name.endswith('.json'):
        messages.error(request, 'This is not a json file')

    prodreview = pd.read_json(io.StringIO(
        json_file.read().decode('utf-8')), lines=True)

    return format(request,prodreview)


def format(request,prodreview):
    reviews = prodreview
    reviews[['HelpfulnessNumerator', 'HelpfulnessDenominator']] = pd.DataFrame(
        reviews.helpful.values.tolist(), index=reviews.index)
    reviews.drop_duplicates(
        subset=['reviewerID', 'asin', 'unixReviewTime'], inplace=True)

    reviews['Helpful %'] = np.where(reviews['HelpfulnessDenominator'] > 0,
                                    reviews['HelpfulnessNumerator'] / reviews['HelpfulnessDenominator'], -1)
    reviews['% Upvote'] = pd.cut(reviews['Helpful %'], bins=[-1, 0, 0.2, 0.4, 0.6, 0.8, 1.0], labels=[
                                 'Empty', '0-20%', '20-40%', '40-60%', '60-80%', '80-100%'], include_lowest=True)
    reviews['Id'] = reviews.index

    import pickle
    file = open('bingo', 'ab')

    pickle.dump(reviews, file)
    file.close()
    return HttpResponseRedirect('/createimage')