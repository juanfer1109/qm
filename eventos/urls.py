from django.urls import path
from . import views

urlpatterns = [
    path('evento/<int:pk>/', views.eventDetails, name="eventos.detail"),
    path('inscribirse/<int:pk>/', views.inscribirse, name="eventos.inscribir"),
    path('desusbribirse/<int:pk>/', views.desuscribirse, name="eventos.desuscribir"),
    path('lista/', views.listaEventos, name="eventos.lista"),
]