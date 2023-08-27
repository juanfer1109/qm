from django.urls import path
from . import views

urlpatterns = [
    path("", views.listaFacturas, name="factura.list"),
    path("nueva/", views.nuevaFactura, name="factura.crear"),
    path("modificar/<int:pk>/", views.modificarFactura, name="factura.modificar"),
    path("borrar/<int:pk>/", views.borrarFactura, name="factura.borrar"),
]
