from django.core import serializers
from polls.models import review
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from rest_framework.parsers import JSONParser
from . models import review
from . serializers import reviewSerializers
import pickle
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from collections import Counter
import nltk
import seaborn as sns
import string
from nltk.corpus import stopwords
import regex as re
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from django.contrib.messages import get_messages
from threading import Thread
import keras.backend.tensorflow_backend as tb
from keras import backend as K
tb._SYMBOLIC_SCOPE.value = True
nltk.download('stopwords')
stop = set(stopwords.words('english'))
from nltk import flatten
from . forms import ReviewForm
import itertools


class ReviewView(viewsets.ModelViewSet):
	queryset = review.objects.all()
	serializer_class = reviewSerializers

def index(request):
    return render(request, "polls/index.html")


@login_required
def dashboard(request):
	 return render(request, "polls/dashboard.html")



def clean_document(doco):
	punctuation = string.punctuation
	punc_replace = ''.join([' ' for s in punctuation])
	doco_link_clean = re.sub(r'http\S+', '', doco)
	doco_clean_and = re.sub(r'&\S+', '', doco_link_clean)
	doco_clean_at = re.sub(r'@\S+', '', doco_clean_and)
	doco_clean = doco_clean_at.replace('-', ' ')
	doco_alphas = re.sub(r'\W +', ' ', doco_clean)
	trans_table = str.maketrans(punctuation, punc_replace)
	doco_clean = ' '.join([word.translate(trans_table) for word in doco_alphas.split(' ')])
	doco_clean = doco_clean.split(' ')
	p = re.compile(r'\s*\b(?=[a-z\d]*([a-z\d])\1{3}|\d+\b)[a-z\d]+', re.IGNORECASE)
	doco_clean = ([p.sub("", x).strip() for x in doco_clean])
	doco_clean = [word.lower() for word in doco_clean if len(word) > 2]
	doco_clean = ([i for i in doco_clean if i not in stop])
	doco_clean = ([p.sub("", x).strip() for x in doco_clean])
	return doco_clean

def lstm_model(text,model):
	model1 = pickle.load(open('lstm_model.pkl','rb'))

	review_clean = clean_document(text)
	#print(review_clean)
	sentences = [' '.join(review_clean)]
	#print(sentence)

	tokenizer = pickle.load(open('tokenizer.pkl','rb'))
	sequence_dict = tokenizer.word_index
	

	review_encoded = [];
	#for i,review in enumerate(review_clean):
	#	review_encoded.append([sequence_dict[x] for x in review]);
	review_encoded.append([sequence_dict[x] for x in review_clean]);
	#print(review_encoded)
	max_cap =8;
	test_data = pad_sequences(review_encoded, maxlen=max_cap, truncating='post')
	np.random.seed(1024);
	random_posit = np.arange(len(test_data))
	np.random.shuffle(random_posit)
	test_data = test_data[random_posit]
	test_result = model1.predict(test_data)

	#print(test_result)

	res = list(itertools.chain(*test_result))
	#print(res)
	K.clear_session()

	return(res)


#@api_view(["POST"])
def sentiment_analysis(text,model):
	try:

		if(model == "Naive Bayes"):
			mdl=pickle.load(open('nb_model.pkl','rb'))
		elif(model == "Random Forest"):
			mdl=pickle.load(open('randomforest_model.pkl','rb'))
		elif(model == "KNN"):
			mdl=pickle.load(open('knn_model.pkl','rb'))
		elif(model == "Gradient Boosting"):
			mdl=pickle.load(open('gradient_model.pkl','rb'))
		elif(model == "SVC"):
			mdl=pickle.load(open('svm_model.pkl','rb'))

		bow_transformer = joblib.load('transformer_model.sav')

	
		#text_data=request.data
		#actual_review = text_data["text"]
		actual_review = text
		review_transformed = bow_transformer.transform([actual_review])


		result = mdl.predict(review_transformed)[0]

		#print(result)
		res = [result]		
		newdf=pd.DataFrame(res, columns=['Status'])
		newdf=newdf.replace({5:'Positive', 1:'Negative'})

		
		#print(newdf)
		#return JsonResponse('The sentiment of this text is {}'.format(newdf.Status[0]), safe=False)
		return (newdf.Status[0])

	except ValueError as e:
		#return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
		return (e.args[0])


@login_required
def userfields(request):
	#request.session.flush()
	if request.method =='POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']
			model = form.cleaned_data['model']
			#print(text)
			if model == "RNN":
				answer = lstm_model(text,model)
				positive = answer[0]*100
				negative = answer[1]*100
				messages.success(request,'The positive sentiment in this review is {:.2f}% and negative sentiment in this review is {:.2f}%'.format(positive,negative))

			else:
				answer = sentiment_analysis(text,model)
				#print(sentiment_analysis(text))
				messages.success(request,'The sentiment of this review is: {}'.format(answer))

				

	form=ReviewForm()
				
	return render(request, 'polls/forms.html', {'form':form})
