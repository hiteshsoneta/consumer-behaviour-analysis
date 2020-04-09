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

global transdf

@login_required
def trans_upload(request):
    template="upload.html"


    if request.method == 'GET':
        return render(request,template)

    csv_file=request.FILES

    csv_file1 = csv_file['file']

    support = request.POST['support']
    confidence = request.POST['confidence']
    lift = request.POST['lift']

    if not csv_file1.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')
    
    

    prodreview = pd.read_csv(io.StringIO(csv_file1.read().decode('utf-8')), delimiter=',')
    
    return reco(prodreview,support,confidence,lift)
   



#@api_view(["POST"])
#@login_required
def reco(unit,support,confidence,lift):
    try:
        #called the prodreview dataset, now calculating transactions from it

        Transactions=pd.DataFrame(columns=['transactions'])

        transactions=[]

        for unique_id,item in zip(unit.asin,unit.related):
            trans = []
            trans.append(unique_id)
            item_dict=ast.literal_eval(item)
            #print(item_dict)
            #print(type(item_dict))

            if "also_bought" in item_dict.keys():
                for i in item_dict['also_bought']:
                    trans.append(i)
            transactions.append(trans)

        Transactions['transactions']=transactions


        trans_list=Transactions['transactions'].values.tolist() #transdf uploaded by user is converted to list

        # trans=[]
        # for j in trans_list:
        #     sub=j.split(',')
        #     trans.append(sub)
        
        #0.0085,0.4,3
        support = float(support)
        confidence = float(confidence)
        lift = float(lift)

        rules = apriori(trans_list, min_support=support, min_confidence=confidence, min_lift=lift,min_length=3)
        results = list(rules)
        

        output = []
        for row in results:
            output.append([str(row.items), "support="+str(row.support), "confidence="+str(row.ordered_statistics[0].confidence), "lift="+str(row.ordered_statistics[0].lift)])
        

        apriori_summary = pd.DataFrame(columns=('Items','Support','Confidence','Lift'))

        Support =[]
        Confidence = []
        Lift = []
        Items = []

        for row in results: 
            Items.append(row.items)
            Support.append(row.support)
            Confidence.append(str(row.ordered_statistics[0].confidence))
            Lift.append(row.ordered_statistics[0].lift)
            

        apriori_summary['Items'] = Items                                   
        apriori_summary['Support'] = Support
        apriori_summary['Confidence'] = Confidence
        apriori_summary['Lift']= Lift

        #return HttpResponse(apriori_summary.to_html())

        #print(ProductReview['asin'])
        names=[]
        for items in apriori_summary.Items:
            name=[]
            for unique in items:
                temp = unit.loc[unit['asin']==str(unique)]
                name.append(list(temp.title))
            names.append(name)
        
        name_df = pd.DataFrame(names)
        
        #print (names)

        AprioriResults = pd.DataFrame.join(apriori_summary,name_df,how='left')

        
        #print(type(AprioriResults_csv)) #string

        
        #with open('apriori.html', 'w') as fo:
         #   fo.write(AprioriResults.to_html())

       # AprioriResults_csv = AprioriResults.to_html()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="apriorisummary.csv"'
        AprioriResults.to_csv(path_or_buf=response,float_format='%.4f',index=False)
        return response

        #<a  href="D:\Anaconda3\envs\gputest\BE proj\AprioriResults" download> Download Document </a>
        #download_csv(AprioriResults)

        #return render(request,'apriori.html')
        #return HttpResponse(AprioriResults_csv)

        
        #return download_csv(AprioriResults)

    except ValueError as e:
        return (e.args[0])
		#return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def download_csv(AprioriResults):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    print(AprioriResults)
    #print(type(AprioriResults))
    AprioriResults.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")

    return response




        


        


    


