from django.shortcuts import render
from datetime import datetime as dt, date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import CustomUser
from eventos.models import Evento, Inscripciones
from eventos.tasks import RecordarPago

def homeView(request):
    RecordarPago()
    staff = False
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
    nickname = ""
    nm = False
    user = request.user
    comunidad = False
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        act_user = User.objects.get(username=user)
        if dt.today().day == cu.birthday.day and dt.today().month == cu.birthday.month:
            cumple = True
        if cu.comunidad:
            comunidad =True
        if act_user.is_staff:
            staff = True
    except:
        pass
    
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        nickname = cu.nickname.capitalize()
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
    for event in Evento.objects.filter(cancelado=False, concluido=False):
        event.cant_inscritos = 0
        for inscripcion in Inscripciones.objects.filter(evento=event):
            event.cant_inscritos = event.cant_inscritos + inscripcion.cantidad
        if event.cant_inscritos >= event.cupos:
            event.cerrado = True

        if event.fecha < date.today():
            event.concluido = True

        event.save()

    return render(request, 'home/welcome.html', {
        'today': fecha,
        'cumple': cumple,
        'nickname': nickname,
        'nm': nm,
        'navidad': navidad,
        'n_year': n_year,
        'comunidad':comunidad,
        'staff': staff,
        'events': Evento.objects.filter(cancelado=False, concluido=False, prueba=False).order_by('fecha'),
        'all_events': Evento.objects.filter(cancelado=False, concluido=False).order_by('fecha'),
    })

def quienesSomos(request):
    comunidad = False
    staff = False
    try:
        user = request.user
        act_user = User.objects.get(username=user)
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad:
            comunidad =True
        if act_user.is_staff:
            staff = True
    except:
        pass

    return render(request, 'home/quienes_somos.html', {
        'comunidad': comunidad,
        'staff': staff,
    })

@login_required
def comunidad(request):
    comunidad = False
    if CustomUser.objects.get(user=request.user).comunidad:
        comunidad =True
        return render(request, 'home/comunidad.html', {
            'comunidad': comunidad,
        })
    else:
        return HttpResponseRedirect(reverse('home'))