from django.urls import path

from . import views

urlpatterns = [
    path("crear_eq/", views.crearEquipo, name="mtto.crear_equipo"),
    path("lista_eq/", views.listadoEquipos, name="mtto.listado_equipos"),
    path("lista_mis_eq/", views.misEquipos, name="mtto.mis_equipos"),
    path("detalle/<int:pk>/", views.detalleEquipo, name="mtto.details"),
    path("<int:pk>/mtto/", views.mtto, name="mtto.mtto"),
    path("crear-mtto/<int:pk>", views.crearMtto, name="mtto.crear_mtto"),
    path("crear-proveedor/", views.crearProveedor, name="mtto.crear_proveedor"),
    path("proveedor/<int:pk>/", views.verProveedor, name="mtto.proveedor"),
    path("listaproveedores/", views.listadoProveedores, name="mtto.lista_proveedores"),
]
