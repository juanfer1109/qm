from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template

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
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    if request.method == 'POST':
        year = int(request.POST['year'].replace('.', '').replace(',', ''))
        amount_donations = 0
        for donation in donations:
            if int(donation.date.year) == int(year):
                amount_donations = amount_donations + donation.value
        permanencia = Permanencia.objects.get(year=year)
        mes = meses[fecha.month-1]
        datos = {
            'comunidad': cu.comunidad,
            'permanencia': permanencia,
            'cu': cu,
            'user': user,
            'fecha': fecha,
            'valor': amount_donations,
            'mes': mes,
        }
        template_path = 'donation/certificado_donacion.html'
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'filename="certificado.pdf"'
        response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'
        template = get_template(template_path)
        html = template.render(datos)
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('Tenemos alguno errores <prep>' + html + '</prep>')
        return response
    
    return render(request, 'donation/donations.html', {
        'permanencias': permanencias,
        'comunidad': cu.comunidad,
    })