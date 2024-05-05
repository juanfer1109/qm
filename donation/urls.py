from django.urls import path

from . import views

urlpatterns = [
    path("", views.donations, name="donations"),
    path("lista/", views.listaDonaciones, name="donations.lista"),
    path("agregar/", views.agregarDonacion, name="donations.agregar"),
    path("permanencias/", views.listaPermanencias, name="donations.lista_permanencias"),
    path("agregperm/", views.apregarPermanencia, name="donations.agregar_permanencia"),
]
