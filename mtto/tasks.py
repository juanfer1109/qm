from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import User
from datetime import date
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from django.template.loader import get_template

from users.models import CustomUser
from .models import Equip

@shared_task(bind=True)
def correoMtto(token):
    users = CustomUser.objects.filter(mtto=True)
    equips = Equip.objects.all().order_by('next_maintenance')
    for equip in equips:
        if equip.next_maintenance is not None:
            days = (equip.next_maintenance - date.today()).days
            if days <= 0:
                for user in users:
                    if user.mtto:
                        subject = 'Mantenimiento Atrasado de ' + equip.name
                        template = render_to_string('mtto/email.html', {
                            'name': user.nickname,
                            'equipo': equip.name,
                            'fecha': equip.next_maintenance,
                            'days': -days,
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

            if (days > 0 and days <= 3) or days == 7 or days == 14 or days == 30 or days == 60:
                for user in users:
                    if user.mtto:
                        subject = 'Próximo Mantenimiento de ' + equip.name
                        template = render_to_string('mtto/email2.html', {
                            'name': user.nickname,
                            'equipo': equip.name,
                            'fecha': equip.next_maintenance,
                            'days': days,
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

@shared_task(bind=True)
def revisarMttos(token):
    for equip in Equip.objects.all():
        days = (equip.next_maintenance - date.today()).days
        if days <= 0:
            equip.atrasado = True
            equip.days_3 = False
            equip.days_7 = False
            equip.days_14 = False
            equip.days_30 = False
            equip.days_60 = False

        if days <= 4 and days > 0:
            equip.days_3 = True
            equip.days_7 = False
            equip.days_14 = False
            equip.days_30 = False
            equip.days_60 = False

        if days == 7:
            equip.days_7 = True
            equip.days_14 = False
            equip.days_30 = False
            equip.days_60 = False

        if days == 14:
            equip.days_14 = True
            equip.days_30 = False
            equip.days_60 = False

        if days == 30:
            equip.days_30 = True
            equip.days_60 = False

        if days == 60:
            equip.days_60 = True

        equip.save()

@shared_task(bind=True)
def correoMtto2(token):
    users = CustomUser.objects.filter(mtto=True)
    equipos = Equip.objects.all().order_by('next_maintenance')
    equipos_atrasados = []
    equipos_3 = []
    equipos_7 = []
    equipos_14 = []
    equipos_30 = []
    equipos_60 = []
    for equipo in equipos:
        if equipo.atrasado:
            equipos_atrasados.append(equipo)
        if equipo.days_3:
            equipos_3.append(equipo)
        if equipo.days_7:
            equipos_7.append(equipo)
        if equipo.days_14:
            equipos_14.append(equipo)
        if equipo.days_30:
            equipos_30.append(equipo)
        if equipo.days_60:
            equipos_60.append(equipo)
        equipo.atrasado = False
        equipo.days_3 = False
        equipo.days_7 = False
        equipo.days_14 = False
        equipo.days_30 = False
        equipo.days_60 = False
        equipo.save()
    for user in users:
        if user.mtto:
            subject = 'Mantenimientos Quintana'
            template = get_template('mtto/email3.html')
            content = template.render({
                'name': user.nickname,
                'equipos_atrasados': equipos_atrasados,
                'atrasados': len(equipos_atrasados) > 0,
                'equipos_3': equipos_3,
                'tres': len(equipos_3) > 0,
                'equipos_7': equipos_7,
                'siete': len(equipos_7) > 0,
                'equipos_14': equipos_14,
                'catorce': len(equipos_14) > 0,
                'equipos_30': equipos_30,
                'treinta': len(equipos_30) > 0,
                'equipos_60': equipos_60,
                'sesenta': len(equipos_60) > 0,
            })
            sendTo = User.objects.get(username=user.user).email
            email = EmailMultiAlternatives(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [sendTo,],
            )
            email.attach_alternative(content, 'text/html')
            email.fail_silently = False
            email.send()