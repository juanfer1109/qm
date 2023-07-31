from django.urls import path

from . import views

urlpatterns = [
    path("", views.homeView, name="home"),
    path("quienes-somos", views.quienesSomos, name="quienes_somos"),
    path("comunidad/", views.comunidad, name="home.comunidad"),
]
