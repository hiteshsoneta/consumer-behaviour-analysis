"""consumerbehaviour URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


urlpatterns = [
    path('', include('polls.urls'),name='index'),
    path('apriori/',include('apriori.urls'),name='apriori'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    #path('upload-csv/',review_upload, name="review_upload"),

    path('upload-country/', user_views.country, name="country"),
    path('upload-city/', user_views.city, name="city"),
    path('pie-chart/', user_views.pie_chart, name='pie-chart'),
    path('home/', user_views.home, name='home'),
    # visualization urls
    path('population-chart/', user_views.population_chart, name='population-chart'),
    path('countrating1/', user_views.countrating1, name='countrating1'),
    path('countrating/', user_views.countrating, name='countrating'),
    path('countrating2/', user_views.countrating2, name='countrating2'),
    path('cntrating/', user_views.cntrating, name='cntrating'),
    path('distprod/<str:prod_id>', user_views.distprod, name='distprod'),
    path('distcust/<str:cust_id>', user_views.distcust, name='distcust'),
    path('enterprodid/', user_views.enterprodid, name='enterprodid'),
    path('entercustid/', user_views.enteruserid, name='entercustid'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
