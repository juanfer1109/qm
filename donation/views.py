from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User

from xhtml2pdf import pisa

from .models import Donation, Permanencia
from users.models import CustomUser


@login_required
def donations(request):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    donations = Donation.objects.filter(user=user)
    permanencias = Permanencia.objects.all()
    fecha = date.today()
    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]

    if request.method == "POST":
        year = int(request.POST["year"].replace(".", "").replace(",", ""))
        amount_donations = 0

        for donation in donations:
            if int(donation.date.year) == int(year):
                amount_donations = amount_donations + donation.value

        if amount_donations == 0:
            messages.success(request, "No tenemos donaciones registradas")
            return HttpResponseRedirect(reverse("donations"))

        permanencia = Permanencia.objects.get(year=year)
        mes = meses[fecha.month - 1]
        datos = {
            "comunidad": cu.comunidad,
            "permanencia": permanencia,
            "cu": cu,
            "user": user,
            "fecha": fecha,
            "valor": amount_donations,
            "mes": mes,
        }
        template_path = "donation/certificado_donacion.html"
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'filename="certificado.pdf"'
        response["Content-Disposition"] = 'attachment; filename="certificado.pdf"'
        template = get_template(template_path)
        html = template.render(datos)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Tenemos alguno errores <prep>" + html + "</prep>")
        return response

    return render(
        request,
        "donation/donations.html",
        {
            "permanencias": permanencias,
            "comunidad": cu.comunidad,
        },
    )


@login_required
def listaDonaciones(request):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.comunidad:
        return HttpResponseRedirect(reverse("home"))
    
    years = set()
    for donation in Donation.objects.all():
        years.add(donation.date.year)

    if request.method =='POST':
        class Donacion():
            def __init__(self, id, nombre, valor):
                self.id = id
                self.nombre = nombre
                self.valor = valor
        
        year = int(request.POST["year"].replace(".", "").replace(",", ""))
        donations = []
        totalDonations = 0
        for donation in Donation.objects.filter(date__year=year):
            totalDonations += donation.value
            if len(donations) == 0:
                donations.append(Donacion(
                    CustomUser.objects.get(user=donation.user).id_number,
                    f'{donation.user.first_name} {donation.user.last_name}',
                    donation.value
                ))
            else:
                check = False
                for i in range(len(donations)):
                    if donations[i].id == CustomUser.objects.get(user=donation.user).id_number:
                        donations[i].valor += donation.value
                        check = True
                        break
                    
                if check == False:
                    donations.append(Donacion(
                        CustomUser.objects.get(user=donation.user).id_number,
                        f'{donation.user.first_name} {donation.user.last_name}',
                        donation.value
                    ))
        
        donations.sort(key=lambda x: x.valor, reverse=True)
        return render(
            request,
            'donation/lista_donaciones.html',
            {
                "data": True,
                "donaciones": donations,
                "years": years,
                "total": totalDonations,
                "comunidad": cu.comunidad,
                "staff": cu.staff,
                "year": year,
            }
        )
    
    return render(
        request,
         'donation/lista_donaciones.html',
         {
            "years": years,
            "data": False,
            "comunidad": cu.comunidad,
            "staff": cu.staff,
         }
         )


@login_required
def agregarDonacion(request):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method =='POST':
        id = request.POST["id"].replace(".", "").replace(",", "")
        try:
            donante = CustomUser.objects.get(id_number=id)
        except:
            return render(
                request,
                'donation/agregar_donacion.html',
                {
                    "comunidad": cu.comunidad,
                    "message": "No existe esa identificación",
                }
            )
        fecha = request.POST["fecha"]
        valor = int(request.POST["valor"].replace(".", "").replace(",", ""))
        don = Donation(user=donante.user, date=fecha, value=valor)
        don.save()
        return render(
        request,
        'donation/agregar_donacion.html',
        {
            "comunidad": cu.comunidad,
            "message": "Donación agregada",
        }
    )
    
    return render(
        request,
        'donation/agregar_donacion.html',
        {
            "comunidad": cu.comunidad,
        }
    )