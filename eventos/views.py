from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date

from users.models import CustomUser
from .models import Evento, Inscripciones

def eventDetails(request, pk):
    comunidad = False
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad == True:
            comunidad =True
    except:
        pass
    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = evento.inscritos.count()
        if evento.cant_inscritos >= evento.cupos:
            evento.cerrado = True

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()

    event = Evento.objects.get(pk=pk)
    inscrito = request.user in event.inscritos.all()

    return render(request, 'eventos/detail.html', {
        'event':event,
        'inscrito': inscrito,
        'comunidad': comunidad,
    })

@login_required
def inscribirse(request, pk):
    if request.method =='POST':
        pago =request.POST["pago"]
        actUser = request.user
        event = Evento.objects.get(pk=pk)
        if CustomUser.objects.get(user=actUser).comunidad:
            return render(request, 'eventos/detail.html', {
                'event': event,
                'message1': 'Los miembros de la comunidad no se deben inscribir'
            })
        
        if event.cerrado:
            return render(request, 'eventos/detail.html', {
                'event': event,
                'message2': 'Lo sentimos, no tenemos cupos para este evento , puedes mirar los otros eventos'
            })

        inscripcion = Inscripciones(usuario=actUser, evento=event, forma_pago=pago)
        inscripcion.save()
        event.inscritos.add(actUser)
        for evento in Evento.objects.filter(cancelado=False, concluido=False):
            evento.cant_inscritos = evento.inscritos.count()
            if evento.cant_inscritos >= evento.cupos:
                evento.cerrado = True

            if evento.fecha < date.today():
                evento.concluido = True

            evento.save()
        return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))
    return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))

@login_required
def desuscribirse(request, pk):
    event = Evento.objects.get(pk=pk)
    actUser = request.user
    event.inscritos.remove(actUser)
    inscripcion = Inscripciones.objects.get(usuario=actUser, evento=event)
    inscripcion.delete()
    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = evento.inscritos.count()
        if evento.cant_inscritos >= evento.cupos:
            evento.cerrado = True

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()
    return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))

def listaEventos(request):
    comunidad = False
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad == True:
            comunidad =True
    except:
        pass

    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = evento.inscritos.count()
        if evento.cant_inscritos >= evento.cupos:
            evento.cerrado = True

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()
    events = Evento.objects.filter(cancelado=False, concluido=False).order_by('fecha')
    return render(request, 'eventos/list.html', {
        'events': events,
        'comunidad': comunidad,
    })