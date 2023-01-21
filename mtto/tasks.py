from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task

from users.models import CustomUser
from .models import Equip

@shared_task(bind=True)
def correoMtto(token):
    print('Juanfer')
    next_mttos = []
    mttos_vencidos =[]
    equips = Equip.objects.all().order_by('next_maintenance')
    for equip in equips:
        if equip.next_maintenance is not None:
            if equip.next_maintenance <= date.today() + timedelta(30) and equip.next_maintenance > date.today():
                next_mttos.append(equip.name + ' ' + str(equip.next_maintenance))
                print(next_mttos)

            if equip.next_maintenance <= date.today():
                mttos_vencidos.append(equip.name + ' ' + str(equip.next_maintenance))
                print(mttos_vencidos)

    users = CustomUser.objects.filter(mtto=True)
    for user in users:
        if user.mtto:
            subject = 'Mantenimientos Pendientes'
            template = render_to_string('mtto/email.html', {
                'name': user.nickname,
                'nexts': next_mttos,
                'vencidos': mttos_vencidos,
                'prox': len(next_mttos) > 0,
                'venc': len(mttos_vencidos) > 0,
                'nothing': len(next_mttos) == 0 and len(mttos_vencidos) == 0,
            })
            sendTo = User.objects.get(username=user.user).email
            email = EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER,
                [sendTo,],
            )
            email.fail_silently = False
            email.send()
    
    return "Done"