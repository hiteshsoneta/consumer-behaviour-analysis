from django.urls import path,include

from . import views

urlpatterns = [
	path('upload-trans/',views.trans_upload,name='trans_upload')
]