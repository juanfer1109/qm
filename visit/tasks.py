from celery import shared_task
from datetime import date, datetime, timedelta
from django.template.loader import get_template
from django.contrib. auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from users.models import CustomUser
from .models import VisitCalendar

@shared_task(bind=True)
def correoVisita(token):
    subject = 'Recuerda tu próxima visita'
    for visita in VisitCalendar.objects.all():
        if visita.date == date.today() + timedelta(days=7):
            user = CustomUser.objects.get(user = visita.visitor.user)
            template = get_template('visit/visita_email.html')
            content = template.render({
                'user': user,
            })
            sendTo = User.objects.get(username=user.user).email
            bcc_email = 'luis.f.bh@hotmail.com'
            email = EmailMultiAlternatives(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [sendTo,],
                bcc=[bcc_email,],
            )
            email.attach_alternative(content, 'text/html')
            email.fail_silently = False
            email.send()
        
        if visita.date == date.today() + timedelta(days=14):
            user = CustomUser.objects.get(user = visita.visitor.user)
            template = get_template('visit/visita_email14.html')
            content = template.render({
                'user': user,
            })
            sendTo = User.objects.get(username=user.user).email
            # bcc_email = 'luis.f.bh@hotmail.com'
            email = EmailMultiAlternatives(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [sendTo,],
                bcc=[bcc_email,],
            )
            email.attach_alternative(content, 'text/html')
            email.fail_silently = False
            email.send()

        if visita.date == date.today() + timedelta(days=21):
            user = CustomUser.objects.get(user = visita.visitor.user)
            template = get_template('visit/visita_email21.html')
            content = template.render({
                'user': user,
            })
            sendTo = User.objects.get(username=user.user).email
            # bcc_email = 'luis.f.bh@hotmail.com'
            email = EmailMultiAlternatives(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [sendTo,],
                bcc=[bcc_email,],
            )
            email.attach_alternative(content, 'text/html')
            email.fail_silently = False
            email.send()