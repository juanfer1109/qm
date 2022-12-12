from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime as dt
from django.shortcuts import redirect
from django.contrib.auth.models import User

from users.models import CustomUser

def homeView(request):
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
    user = request.user
    cu = CustomUser.objects.get(user_id=user.id)
    if dt.today().day == cu.birthday.day and dt.today().month == cu.birthday.month:
        cumple = True

    mes = meses.get(dt.today().month)
    fecha = str(dt.today().day) + " de " + mes + " de " + str(dt.today().year)
    return render(request, 'home/welcome.html', {
        'today': fecha,
        'cumple': cumple
    })
