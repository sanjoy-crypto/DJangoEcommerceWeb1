from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('addtoshopcart/<int:id>/', addtoshopcart, name="addtoshopcart"),
    path('deletefromcart/<int:id>/', deletefromcart, name='deletefromcart'),
    path('orderproduct/', orderproduct, name='orderproduct'),
]
