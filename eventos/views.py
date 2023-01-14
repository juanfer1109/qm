from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth.models import User

from users.models import CustomUser
from .models import Evento, Inscripciones

def eventDetails(request, pk):
    comunidad = False # Por defecto los usuarios no son de la comunidad
    doc = False # Por defecto que no se tiene el documento de identidad del usuario
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad:
            comunidad =True # Se cambia a verdadero si el usuario es de la comunidad
        if cu.id_number != None and cu.id_number != 0:
            doc = True # Se cambia a verdadero si el usuario ya tiene ingresado el documento de identidad
    except:
        pass
    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = evento.inscritos.count()
        if evento.cant_inscritos >= evento.cupos:
            evento.cerrado = True
        else:
            evento.cerrado = False

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()

    event = Evento.objects.get(pk=pk)
    if event.prueba and not(User.objects.get(username=user).is_staff):
        return HttpResponseRedirect(reverse('eventos.lista')) # Si el evento está en prueba y el usuario no es del staff no se muestra el evento

    inscrito = request.user in event.inscritos.all()

    return render(request, 'eventos/detail.html', {
        'event':event,
        'inscrito': inscrito,
        'comunidad': comunidad,
        'doc': doc,
    })

@login_required
def inscribirse(request, pk):
    doc = False
    if request.method =='POST':
        actUser = request.user
        cu = CustomUser.objects.get(user=actUser)
        try:
            cu.id_number = request.POST["id"]
            cu.doc_type = request.POST["tipo_id"]
            cu.save()
            doc = True
        except:
            pass

        pago = request.POST["pago"]
        event = Evento.objects.get(pk=pk)
        if cu.comunidad:
            return render(request, 'eventos/detail.html', {
                'event': event,
                'message1': 'Los miembros de la comunidad no se deben inscribir',
                'doc': doc,
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
            else:
                evento.cerrado = False

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
    try:
        Inscripciones.objects.get(usuario=actUser, evento=event).delete()
    except:
        pass
    
    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = evento.inscritos.count()
        if evento.cant_inscritos >= evento.cupos:
            evento.cerrado = True
        else:
            evento.cerrado = False

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()
    return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))

def listaEventos(request):
    staff = False
    comunidad = False
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad:
            comunidad = True
        if User.objects.get(username=user).is_staff:
            staff = True
    except:
        pass

    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = evento.inscritos.count()
        if evento.cant_inscritos >= evento.cupos:
            evento.cerrado = True
        else:
            evento.cerrado = False

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()
    return render(request, 'eventos/list.html', {
        'events': Evento.objects.filter(cancelado=False, concluido=False, prueba=False).order_by('fecha'),
        'all_events': Evento.objects.filter(cancelado=False, concluido=False).order_by('fecha'),
        'comunidad': comunidad,
        'staff': staff,
    })