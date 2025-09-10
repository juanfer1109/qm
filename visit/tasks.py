import random
from celery import shared_task
from datetime import date, datetime, timedelta
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from users.models import CustomUser
from .models import VisitCalendar


@shared_task(bind=True)
def correoVisita(token):
    subject = "Recuerda tu próxima visita"
    for visita in VisitCalendar.objects.all():
        if visita.date == date.today() + timedelta(days=7):
            user = CustomUser.objects.get(user=visita.visitor.user)
            template = get_template("visit/visita_email.html")
            content = template.render(
                {
                    "user": user,
                }
            )
            sendTo = User.objects.get(username=user.user).email
            bcc_email = "luis.f.bh@hotmail.com"
            email = EmailMultiAlternatives(
                subject,
                "",
                settings.EMAIL_HOST_USER,
                [
                    sendTo,
                ],
                bcc=[
                    bcc_email,
                ],
            )
            email.attach_alternative(content, "text/html")
            email.fail_silently = False
            email.send()

        if visita.date == date.today() + timedelta(days=14):
            user = CustomUser.objects.get(user=visita.visitor.user)
            template = get_template("visit/visita_email14.html")
            content = template.render(
                {
                    "user": user,
                }
            )
            sendTo = User.objects.get(username=user.user).email
            bcc_email = "luis.f.bh@hotmail.com"
            email = EmailMultiAlternatives(
                subject,
                "",
                settings.EMAIL_HOST_USER,
                [
                    sendTo,
                ],
                # bcc=[bcc_email,],
            )
            email.attach_alternative(content, "text/html")
            email.fail_silently = False
            email.send()

        if visita.date == date.today() + timedelta(days=21):
            user = CustomUser.objects.get(user=visita.visitor.user)
            template = get_template("visit/visita_email21.html")
            content = template.render(
                {
                    "user": user,
                }
            )
            sendTo = User.objects.get(username=user.user).email
            bcc_email = "luis.f.bh@hotmail.com"
            email = EmailMultiAlternatives(
                subject,
                "",
                settings.EMAIL_HOST_USER,
                [
                    sendTo,
                ],
                # bcc=[bcc_email,],
            )
            email.attach_alternative(content, "text/html")
            email.fail_silently = False
            email.send()


@shared_task(bind=True)
def generarVisita(token):
    visits = VisitCalendar.objects.filter(date__gte=date.today())
    last_date = date.today()
    for visit in visits:
        if visit.date > last_date:
            last_date = visit.date
            last_miembro = visit.visitor
    if last_date < date.today() + timedelta(days=120):
        comunidad = CustomUser.objects.filter(visit_resp=True)
        list_of_members = []
        for usuario in comunidad:
            list_of_members.append(usuario.user)
            
        random.shuffle(list_of_members)
        i = 0
        j = 0
        k = 0
        while k == 0:
            k = 1
            while j == 0:
                j = 1
                while i < len(list_of_members):
                    miembro = CustomUser.objects.get(user=list_of_members[i])
                    if i + 1 < len(list_of_members) and miembro.pareja:
                        if list_of_members[i + 1] == miembro.pareja.user:
                            random.shuffle(list_of_members)
                            i = -1
                            j = 0
                    i += 1
            if last_miembro.user == list_of_members[0]:
                random.shuffle(list_of_members)
                k = 0
                j = 0
                i = 0
                
        subject = "Se te ha asignado una nueva visita"
        for user in list_of_members:
            last_date = last_date + timedelta(days=7)
            miembro = CustomUser.objects.get(user=user)
            new_visit = VisitCalendar(visitor=miembro, date=last_date)
            new_visit.save()
            template = get_template("visit/nueva_visita.html")
            content = template.render(
                {
                    "user": miembro,
                    "visit": new_visit,
                }
            )
            sendTo = User.objects.get(username=miembro.user).email
            email = EmailMultiAlternatives(
                subject,
                "",
                settings.EMAIL_HOST_USER,
                [
                    sendTo,
                ],
            )
            email.attach_alternative(content, "text/html")
            email.fail_silently = False
            email.send()
