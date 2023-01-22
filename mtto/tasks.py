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