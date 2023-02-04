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
    cumples = CustomUser.objects.filter(mailing_list=True)
    for cumple in cumples:
        if cumple.birthday.day == date.today().day and cumple.birthday.month == date.today().month:
            template = get_template('home/birthday_email.html')
            content = template.render({
                'user': cumple,
            })
            sendTo = User.objects.get(username=cumple.user).email
            bcc_email = 'quintanamagica@gmail.com'
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

@shared_task(bind=True)
def cumpleaños_semana(token):
    cumples = CustomUser.objects.all()
    class this_birthday:
        def __init__(self, name, birthday):
            self.birthday = birthday
            self.name = name

    list = []
    for cumple in cumples:
        if (cumple.birthday.replace(year=date.today().year) - date.today()).days >= 0:
            days = (cumple.birthday.replace(year=date.today().year) - date.today()).days
            birthday = cumple.birthday.replace(year=date.today().year)
        else:
            days = (cumple.birthday.replace(year=date.today().year + 1) - date.today()).days
            birthday = cumple.birthday.replace(year=date.today().year)

        if days > 0 and days <= 7:
            birthday = this_birthday(cumple.nickname, birthday)
            list.append(birthday)
    
    if len(list) > 0:
        comunidad = CustomUser.objects.filter(comunidad=True)
        for miembro in comunidad:
            subject = 'Cumpleaños de esta semana'
            template = get_template('home/cumples_semana.html')
            content = template.render({
                'name': miembro.nickname,
                'list': list,
            })
            sendTo = User.objects.get(username=miembro.user).email
            email = EmailMultiAlternatives(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                [sendTo,],
            )
            email.attach_alternative(content, 'text/html')
            email.fail_silently = False
            email.send()