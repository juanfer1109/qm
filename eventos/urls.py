from django.urls import path
from . import views

urlpatterns = [
    path("evento/<int:pk>/", views.eventDetails, name="eventos.detail"),
    path("inscribirse/<int:pk>/", views.inscribirse, name="eventos.inscribir"),
    path("desusbribirse/<int:pk>/", views.desuscribirse, name="eventos.desuscribir"),
    path("lista/", views.listaEventos, name="eventos.lista"),
    path("agregar_cupo/<int:pk>/", views.agregarCupo, name="eventos.agregar_cupo"),
    path("quitar_cupo/<int:pk>/", views.quitarCupo, name="eventos.quitar_cupo"),
    path("crear/", views.crearEvento, name="eventos.crear"),
    path("editar/<int:pk>/", views.editarEvento, name="eventos.editar"),
    path("eliminar/<int:pk>/", views.borrarEvento, name="eventos.eliminar"),
]
