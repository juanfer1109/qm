from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from users.models import CustomUser
from .models import Factura
from .forms import facturaForm

@login_required
def listaFacturas(request):
    cu = CustomUser.objects.get(user=request.user)
    if cu.comunidad == True:
        facturas = Factura.objects.all().order_by("-date")
    else:
        return HttpResponseRedirect(reverse("home"))
    
    return render(
        request,
        "factura/list.html",
        {
            "facturas": facturas,
            "comunidad": cu.comunidad,
            "nickname": cu.nickname,
        },
    )
    

@login_required
def nuevaFactura(request):
    cu = CustomUser.objects.get(user=request.user)
    if cu.comunidad == False:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        user = CustomUser.objects.get(user=request.user)
        proveedor = request.POST["proveedor"]
        date = request.POST["date"]
        valor = int(request.POST["valor"].replace(".", "").replace(",", ""))
        numero = request.POST["numero"]
        factura = Factura(user=user, date=date, proveedor=proveedor, numero= numero, valor=valor)
        factura.save()
        return redirect("factura.list")
    
    
    return render(
        request,
        "factura/crear_factura.html",
        {
            "comunidad": cu.comunidad,
            "nickname": cu.nickname,
        },
    )

@login_required
def modificarFactura(request, pk):
    cu = CustomUser.objects.get(user=request.user)
    if cu.comunidad == False:
        return HttpResponseRedirect(reverse("home"))
    
    factura = Factura.objects.get(pk=pk)
    fecha = f"{factura.date.year}-{factura.date.month:02d}-{factura.date.day:02d}"
    if request.method == "POST":
        factura.proveedor = request.POST["proveedor"]
        factura.date = request.POST["date"]
        factura.valor = int(request.POST["valor"].replace(".", "").replace(",", ""))
        factura.numero = request.POST["numero"]
        message = None
        if cu != factura.user:
            message = "Solo " + factura.user.nickname + " puede modificar esta factura"
            return render(
                request,
                "factura/modificar_factura.html",
                {
                    "factura": factura,
                    "comunidad": cu.comunidad,
                    "message": message,
                    "fecha": fecha,
                },
            )

        if factura.pagada:
            message = "Factura Pagada"
            return render(
                request,
                "factura/modificar_factura.html",
                {
                    "factura": factura,
                    "comunidad": cu.comunidad,
                    "message": message,
                    "fecha": fecha,
                },
            )

        factura.save()
        return render(
            request,
            "factura/modificar_factura.html",
            {
                "factura": factura,
                "fecha": fecha,
                "comunidad": cu.comunidad,
            },
        )
    else:
        return render(
            request,
            "factura/modificar_factura.html",
            {
                "factura": factura,
                "comunidad": cu.comunidad,
                "fecha": fecha,
            },
        )
    
    
    

@login_required
def borrarFactura(request, pk):
    cu = CustomUser.objects.get(user=request.user)
    if cu.comunidad == False:
        return HttpResponseRedirect(reverse("home"))
    factura = Factura.objects.get(pk=pk)
    fecha = f"{factura.date.year}-{factura.date.month:02d}-{factura.date.day:02d}"
    if cu != factura.user:
        message = "Solo " + factura.user.nickname + " puede modificar esta factura"
        return render(
            request,
            "factura/modificar_factura.html",
            {
                "factura": factura,
                "comunidad": cu.comunidad,
                "message": message,
                "fecha": fecha,
            },
        )

    if factura.pagada:
        message = "Factura Pagada"
        return render(
            request,
            "factura/modificar_factura.html",
            {
                "factura": factura,
                "comunidad": cu.comunidad,
                "message": message,
                "fecha": fecha,
            },
        )
    
    factura.delete()
    facturas = Factura.objects.all().order_by("-date")
    return render(
        request,
        "factura/list.html",
        {
            "facturas": facturas,
            "comunidad": cu.comunidad,
            "nickname": cu.nickname,
        },
    )