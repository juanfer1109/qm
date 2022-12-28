from django.shortcuts import render
from datetime import date
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Issue, Article
from django.contrib.auth.models import User
from users.models import CustomUser

def listOfIssues(request, ed):
    boletin = Issue.objects.get(ed=ed)
    return render(request, 'boletin/boletin.html', {
        'fecha':  date.today(),
        'boletin': boletin,
    })

def sendMail(request):
    users = User.objects.filter(is_active=True)

    for user in users:
        p = CustomUser.objects.get(user=user)
        if p.mailing_list:
            message = f'Hola {p.nickname}'
            # send_mail(
            # 'Test',
            # message,
            # 'jfarangou@gmail.com',
            # [user.email],
            # fail_silently=True,
            # )
    return render(request, 'boletin/users.html', {
            'users': list,
        })
    return HttpResponseRedirect(reverse('home'))