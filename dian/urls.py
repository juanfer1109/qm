from django.urls import path

from . import views

urlpatterns = [
    path('dian', views.docsDian, name='dian.docs'),
    
]