from celery import shared_task
from datetime import date
from django.template.loader import get_template
from django.contrib. auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from users.models import CustomUser

@shared_task(bind=True)
def cumpleaños(token):
    subject = '¡Feliz cumpleaños!'
    cumples = CustomUser.objects.all()
    for cumple in cumples:
        if cumple.birthday.day == date.today().day and cumple.birthday.month == date.today().month:
            template = get_template('home/birthday_email.html')
            content = template.render({
                'user': cumple,
            })
            sendTo = User.objects.get(id=cumple.id).email
            email = EmailMultiAlternatives(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [sendTo,],
            )
            email.attach_alternative(content, 'text/html')
            email.fail_silently = False
            email.send()