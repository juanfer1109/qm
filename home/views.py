from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime as dt
from django.shortcuts import redirect
from django.contrib.auth.models import User

from users.models import CustomUser

def homeView(request):
    n_year = False
    navidad = False
    meses = {
        1:'Enero',
        2: 'Febrero',
        3:'Marzo',
        4:'Abril',
        5:'Mayo',
        6:'Junio',
        7:'Julio',
        8:'Agosto',
        9:'Septiembre',
        10:'Octubre',
        11:'Noviembre',
        12:'Diciembre',
    }
    cumple = False
    nickname = 'Juanfer'
    nm = False
    user = request.user
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        if dt.today().day == cu.birthday.day and dt.today().month == cu.birthday.month:
            cumple = True
    except:
        pass
    
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        nickname = cu.nickname
        nm = True
    except:
        nm = False

    if dt.today().month == 12:
        if dt.today().day == 24 or dt.today().day == 25:
            navidad = True
        elif dt.today().day == 31:
            n_year = True

    if dt.today().month == 1 and dt.today().day == 1:
        n_year = True

    mes = meses.get(dt.today().month)
    fecha = str(dt.today().day) + " de " + mes + " de " + str(dt.today().year)
    return render(request, 'home/welcome.html', {
        'today': fecha,
        'cumple': cumple,
        'nickname': nickname,
        'nm': nm,
        'navidad': navidad,
        'n_year': n_year,
    })

def quienesSomos(request):
    return render(request, 'home/quienes_somos.html')
