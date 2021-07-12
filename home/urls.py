from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('about/', aboutUs, name="about"),
    path('contact/', contactUs, name="contact"),
    path('search/', search, name="search"),
    path('search_auto/', search_auto, name="search_auto"),
    path('category/<int:id>/<slug:slug>/',
         category_products, name="category_products"),
    path('product_details/<int:id>/<slug:slug>/',
         product_details, name="product_details"),


]
