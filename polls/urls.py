from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('polls', views.ReviewView)

urlpatterns = [
    path('', views.index, name='index'),
    #path('pivot_dashboard', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    #path('data', views.pivot_data, name='pivot_data'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('form/', views.userfields, name='sentimentanalysisform'),
    path('api/', include(router.urls)),
    path('status/', views.sentiment_analysis),
]
