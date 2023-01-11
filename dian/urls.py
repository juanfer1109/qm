from django.urls import path

from . import views

urlpatterns = [
    path('docs/', views.docsDian, name='dian.docs'),
]