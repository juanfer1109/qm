from django.urls import path
from . import views

urlpatterns = [
    path("", views.listOfVisits, name="visit.list"),
    path("detail/<int:pk>/", views.visitDetails, name="visit.details"),
    path("input/", views.visitInput, name="visit.input"),
    path("mov/<int:pk>/", views.MovementInput, name="visit.create_movement"),
    path("modify/<int:pk>/", views.modificarVisita, name="visit.modify"),
    path("delete/mov/<int:pk>/", views.borrarMov, name="movement.delete"),
    path("modify/mov/<int:pk>/", views.modificarMov, name="movement.modify"),
    path("calendar/", views.calendarOfVisits, name="visit.calendar"),
    path("calendar/<int:pk>/", views.EditCalendar, name="visit.calendar.edit"),
    path("myvisits/", views.myVisits, name="visit.myvisits"),
    path("datos-contabilidad/", views.datosContabilidad, name="visit.datos_contabilidad"),
    path("delete/<int:pk>/", views.eliminarVisita, name="visit.delete"),
]
