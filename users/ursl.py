from django.urls import path,include

from . import views as user_views

urlpatterns = [
	

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)