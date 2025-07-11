from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from datetime import timedelta, datetime

from .models import Equip, Maintenance, Supplier
from users.models import CustomUser


@login_required
def crearEquipo(request):
    comunidad = False
    if CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff:
        comunidad = True
        if CustomUser.objects.get(user=request.user).mtto:
            miembros = CustomUser.objects.filter(comunidad=True)
            if request.method == "POST":
                name = request.POST["name"].title()
                frequency = request.POST["frequency"]
                responsable = CustomUser.objects.get(user=request.POST["responsable"])
                equipo = Equip(name=name, frequency=frequency, responsable=responsable)
                try:
                    equipo.next_maintenance = request.POST["next_maintenance"]
                except:
                    pass

                equipo.save()
                return HttpResponseRedirect(reverse("mtto.listado_equipos"))

            return render(
                request,
                "mtto/crear_equipo.html",
                {
                    "comunidad": comunidad,
                    "miembros": miembros,
                },
            )
        else:
            messages.success(
                request, "Solo el equipo de mantenimiento puede agregar equipos"
            )
            return HttpResponseRedirect(reverse("mtto.listado_equipos"))
    else:
        return HttpResponseRedirect(reverse("home"))


@login_required
def listadoEquipos(request):
    comunidad = False
    if CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff:
        comunidad = True
        return render(
            request,
            "mtto/listado_equipos.html",
            {
                "equipos": Equip.objects.exclude(next_maintenance=None).order_by("next_maintenance"),
                "comunidad": comunidad,
            },
        )
    else:
        return HttpResponseRedirect(reverse("home"))


@login_required
def detalleEquipo(request, pk):
    comunidad = False
    if CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff:
        comunidad = True
        equipo = Equip.objects.get(pk=pk)
        mttos = Maintenance.objects.filter(equip=equipo).order_by("-date")
        return render(
            request,
            "mtto/detalle_eq.html",
            {
                "equipo": equipo,
                "comunidad": comunidad,
                "mttos": mttos,
            },
        )
    else:
        return HttpResponseRedirect(reverse("home"))


@login_required
def mtto(request, pk):
    comunidad = False
    if CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff:
        comunidad = True
        mtto = Maintenance.objects.get(pk=pk)
        return render(
            request,
            "mtto/mtto.html",
            {
                "mtto": mtto,
                "user": CustomUser.objects.get(user=mtto.user.id).nickname,
                "comunidad": comunidad,
            },
        )
    return HttpResponseRedirect(reverse("home"))


@login_required
def crearMtto(request, pk):
    comunidad = False
    user = request.user
    if CustomUser.objects.get(user=user).comunidad or CustomUser.objects.get(user=user).staff or request.user.is_staff:
        comunidad = True
        if CustomUser.objects.get(user=user).mtto:
            equipo = Equip.objects.get(pk=pk)
            if request.method == "POST":
                supplier = Supplier.objects.get(name=request.POST["supplier"])
                date = request.POST["date"]
                value = request.POST["value"]
                if (
                    equipo.last_maintenance == None
                    or equipo.last_maintenance
                    < datetime.strptime(date, "%Y-%m-%d").date()
                ):
                    equipo.last_maintenance = date
                    equipo.last_value = value
                    equipo.next_maintenance = datetime.strptime(
                        date, "%Y-%m-%d"
                    ) + timedelta(equipo.frequency)
                    equipo.days_60 = False
                    equipo.days_30 = False
                    equipo.days_14 = False
                    equipo.days_7 = False
                    equipo.days_3 = False
                    equipo.atrasado = False
                    equipo.save()

                notes = request.POST["notes"]
                mtto = Maintenance(user=user, equip=equipo, supplier=supplier)
                mtto.date = date
                mtto.value = value
                mtto.notes = notes
                mtto.save()

            listOfSuppliers = Supplier.objects.values_list("name", flat=True).distinct()
            return render(
                request,
                "mtto/crear_mtto.html",
                {
                    "suppliers": listOfSuppliers,
                    "equipo": equipo,
                    "comunidad": comunidad,
                },
            )
        else:
            messages.success(
                request, "Solo el equipo de mantenimiento puede agregar mantenimientos"
            )
            return redirect("mtto.details", pk)
    return HttpResponseRedirect(reverse("home"))


@login_required
def crearProveedor(request):
    comunidad = False
    user = request.user
    if CustomUser.objects.get(user=user).comunidad or CustomUser.objects.get(user=user).staff or request.user.is_staff:
        comunidad = True
        if CustomUser.objects.get(user=user).mtto:
            if request.method == "POST":
                name = request.POST["name"]
                address = request.POST["address"]
                try:
                    phone = int(
                        request.POST["phone"]
                        .replace(".", "")
                        .replace(",", "")
                        .replace(" ", "")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("-", "")
                    )
                except:
                    messages.success(request, "Teléfono Invalido")
                    return redirect("mtto.crear_proveedor")

                contact = request.POST["contact"]
                proveedor = Supplier(
                    name=name, address=address, phone_number=phone, contact=contact
                )
                proveedor.save()
                return HttpResponseRedirect(reverse("mtto.listado_equipos"))

            return render(
                request,
                "mtto/crear_proveedor.html",
                {
                    "comunidad": comunidad,
                },
            )
        messages.success(
            request, "Solo el equipo de mantenimiento puede agregar proveedores"
        )
        return redirect("mtto.lista_proveedores")
    return HttpResponseRedirect(reverse("home"))


@login_required
def listadoProveedores(request):
    if CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff:
        return render(
            request,
            "mtto/listado_proveedores.html",
            {
                "comunidad": CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff,
                "suppliers": Supplier.objects.all(),
            },
        )
    return HttpResponseRedirect(reverse("home"))


@login_required
def verProveedor(request, pk):
    if CustomUser.objects.get(user=request.user).comunidad or CustomUser.objects.get(user=request.user).staff or request.user.is_staff:
        return render(
            request,
            "mtto/proveedor.html",
            {
                "comunidad": CustomUser.objects.get(user=request.user).comunidad,
                "supplier": Supplier.objects.get(pk=pk),
            },
        )
    return HttpResponseRedirect(reverse("home"))


@login_required
def misEquipos(request):
    user = CustomUser.objects.get(user=request.user)
    comunidad = False
    if user.comunidad or user.staff or request.user.is_staff:
        comunidad = True
        return render(
            request,
            "mtto/mis_equipos.html",
            {
                "equipos": Equip.objects.filter(responsable=user).order_by(
                    "next_maintenance"
                ),
                "comunidad": comunidad,
            },
        )
    else:
        return HttpResponseRedirect(reverse("home"))
