from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
#from . forms import MyForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import json
import ast
import numpy as np
from sklearn import preprocessing
import pandas as pd
from apyori import apriori
from django_pandas.managers import DataFrameManager
from django.http import HttpResponse
import csv,io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

import pandas as pd
import numpy as np
from pandas import DataFrame 
import nltk
#import torch
import pickle
#from models import RBM

#import torch.nn as nn
#import torch.nn.parallel
#import torch.optim as optim
#import torch.utils.data
#from torch.autograd import Variable

global transdf

@login_required
def rbm_upload(request):
    template="upload_rbm.html"


    if request.method == 'GET':
        return render(request,template)

    csv_file=request.FILES

    csv_file1 = csv_file['file']


    if not csv_file1.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')
    
    

    prodreview = pd.read_csv(io.StringIO(csv_file1.read().decode('utf-8')), delimiter=',')
    
    return reco(prodreview)
   

def convert(data):
    new_data=[]
    for id_users in range(1,nb_users+1):
        id_products = data[:,1][data[:,0]==id_users]
        id_ratings = data[:,2][data[:,0]==id_users]
        ratings = np.zeros(nb_products)
        ratings[id_products-1]=id_ratings
        new_data.append(list(ratings))
    return new_data



#@api_view(["POST"])
#@login_required
def reco(reviews):
    try:

        #converting dataframe to required format
        dfreviews = reviews[["reviewerID","asin","overall"]]
        dfreviews = dfreviews.sort_values(by = 'reviewerID')
        dfreviews.reset_index(drop=True,inplace=True)

        #considering asin which have above 100 reviews
        count_asin = dfreviews.groupby("asin", as_index=False).count().rename(columns={"reviewerID":"totalReviewers"}).drop(columns=["overall"])
        dfreviews = pd.merge(dfreviews, count_asin, how='right', on='asin')
        dfreviews = dfreviews[dfreviews.totalReviewers >= 100]

        #considering reviewers who have given more than 5 reviews
        count = dfreviews.groupby("reviewerID", as_index=False).count().rename(columns={"asin":"totalReviews"}).drop(columns=["totalReviewers","overall"])
        dfreviews = pd.merge(dfreviews, count, how='right', on='reviewerID')
        dfreviews = dfreviews[dfreviews.totalReviews >= 5]


        unique_reviewers = dfreviews.reviewerID.unique()
        unique_reviewers = pd.DataFrame(data=unique_reviewers)
        unique_reviewers = unique_reviewers.rename(columns={0:'reviewerID'})
        unique_reviewers.reset_index(drop=True,inplace=True)
        unique_reviewers.index = np.arange(1,len(unique_reviewers)+1)
        unique_reviewers['ind']=unique_reviewers.index


        dfReviews = pd.merge(dfreviews,unique_reviewers,how='inner',on=['reviewerID'])

        unique_asin = dfreviews.asin.unique()
        unique_asin = pd.DataFrame(data=unique_asin)
        unique_asin = unique_asin.rename(columns={0:'asin'})
        unique_asin['asin_ind']=unique_asin.index
        unique_asin.asin_ind = np.arange(1,len(unique_asin)+1)

        dfReviews = pd.merge(dfReviews,unique_asin,how='inner',on=['asin'])



        dfReviews['reviewerID'] = dfReviews['ind']
        dfReviews['asin']=dfReviews['asin_ind']
        dfReviews = dfReviews.drop(columns=["ind","asin_ind","totalReviews","totalReviewers"])
        dfReviews.reset_index(drop=True,inplace=True)

       

        from sklearn.model_selection import train_test_split
        training_set,test_set = train_test_split(dfReviews,test_size = 0.2,random_state=0)

        training_set = training_set.sort_values(by = 'reviewerID')
        training_set.reset_index(drop=True,inplace=True)
        test_set = test_set.sort_values(by = 'reviewerID')
        test_set.reset_index(drop=True,inplace=True)

        #Making a copy of test set dataframe for backtracking
        #test_set_df = test_set

        training_set = np.array(training_set,dtype="int")
        test_set = np.array(test_set,dtype="int")

        
        nb_users = len(dfReviews.reviewerID.value_counts())
        nb_products = len(dfReviews.asin.value_counts())

        #training_set = convert(training_set)
        #test_set = convert(test_set)

        # Converting the data into Torch tensors
        #training_set = torch.FloatTensor(training_set)
        #test_set = torch.FloatTensor(test_set)

        #Converting the ratings into binary ratings 1(liked) and 0(not liked)
        #training_set[training_set == 0] = -1
        #training_set[training_set == 1] = 0
        #training_set[training_set == 2] = 0
        #training_set[training_set >= 3] = 1


        #test_set[test_set == 0] = -1
        #test_set[test_set == 1] = 0
        #test_set[test_set == 2] = 0
        #test_set[test_set >= 3] = 1

        #rbm = pickle.load(open('rbm.pkl','rb'))
        
        #pred_set = rbm.predict(test_set).numpy()

        recommendations = pd.read_csv("rbm_recommendations.csv")
    

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rbm_recommendations.csv"'
        recommendations.to_csv(path_or_buf=response,float_format='%.4f',index=False)



        return response


    except ValueError as e:
        return (e.args[0])
		#return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def download_csv(recommendations):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    #print(AprioriResults)
    #print(type(AprioriResults))
    recommendations.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")

    return response




        


        


    


