from django.urls import path
from . import views

urlpatterns = [
    path("", views.listaDocumentos, name="documentos.list"),
    path("nuevotipo/", views.nuevoTipo, name="documentos.nuevotipo"),
    path("borrartipo/<int:pk>/", views.borrarTipo, name="documentos.borrartipo"),
    path("borrardocumento/<int:pk>/", views.borrarDocumento, name="documentos.borrardocumento"),
    path("nuevodocumento/", views.nuevoDoc, name="documentos.nuevodocumento"),
]
