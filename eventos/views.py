from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from users.models import CustomUser
from .models import Evento, Inscripciones

def eventDetails(request, pk):
    comunidad = False # Por defecto los usuarios no son de la comunidad
    doc = False # Por defecto que no se tiene el documento de identidad del usuario
    try:
        user = request.user # Usuario loggeado
        cu = CustomUser.objects.get(user=user) # Custom User del usuario loggeado
        if cu.comunidad:
            comunidad =True # Se cambia a verdadero si el usuario es de la comunidad
        if cu.id_number != None and cu.id_number != 0:
            doc = True # Se cambia a verdadero si el usuario ya tiene ingresado el documento de identidad
    except:
        pass

    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = 0
        for inscripcion in Inscripciones.objects.filter(evento=evento):
                evento.cant_inscritos = evento.cant_inscritos + inscripcion.cantidad
        if evento.cant_inscritos >= evento.cupos or evento.fecha_costo2 < date.today():
            evento.cerrado = True
        else:
            evento.cerrado = False

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()

    event = Evento.objects.get(pk=pk)
    if event.fecha_costo1 > date.today():
        event.costo = event.costo1
        event.fecha_costo = event.fecha_costo1
    else:
        event.costo = event.costo2
        event.fecha_costo = event.fecha_costo2
    
    event.save()

    if event.prueba: 
        try:
            staff = cu.staff
        except:
            staff = False
        if not staff:
            return HttpResponseRedirect(reverse('eventos.lista')) # Si el evento está en prueba y el usuario no es del staff no se muestra el evento

    inscrito = request.user in event.inscritos.all()
    try:
        cupos = Inscripciones.objects.get(usuario=request.user, evento=event).cantidad
    except:
        cupos = 0

    return render(request, 'eventos/detail.html', {
        'event':event,
        'inscrito': inscrito,
        'cupos': cupos,
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

        inscripcion = Inscripciones(usuario=actUser, evento=event) #, forma_pago=pago)
        subject = 'Gracias por tu inscripción'
        template = get_template('eventos/email_inscripcion.html')
        content = template.render({
            'name': cu.nickname,
            'evento': event,
        })
        sendTo = User.objects.get(username=actUser.username).email
        bcc_email = 'quintanamagica@gmail.com'
        email = EmailMultiAlternatives(
            subject,
            '',
            settings.EMAIL_HOST_USER,
            [sendTo,],
            bcc=[bcc_email],
        )
        email.attach_alternative(content, 'text/html')
        email.fail_silently = False
        email.send()
        
        inscripcion.save()
        event.inscritos.add(actUser)
        for evento in Evento.objects.filter(cancelado=False, concluido=False):
            evento.cant_inscritos = 0
            for inscripcion in Inscripciones.objects.filter(evento=evento):
                evento.cant_inscritos = evento.cant_inscritos + inscripcion.cantidad
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
    actUser = request.user
    event = Evento.objects.get(pk=pk)
    if not(Inscripciones.objects.get(usuario=actUser, evento=event).pago_recibido):
        event.inscritos.remove(actUser)
        try:
            Inscripciones.objects.get(usuario=actUser, evento=event).delete()
        except:
            pass
        
        for evento in Evento.objects.filter(cancelado=False, concluido=False):
            evento.cant_inscritos = 0
            for inscripcion in Inscripciones.objects.filter(evento=evento):
                evento.cant_inscritos = evento.cant_inscritos + inscripcion.cantidad
            if evento.cant_inscritos >= evento.cupos:
                evento.cerrado = True
            else:
                evento.cerrado = False

            if evento.fecha < date.today():
                evento.concluido = True

            evento.save()
        return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))
    
    messages.success(request, "Como ya recibimos tu donación para desuscribirte a la experiencia comunicate con nosotros")
    return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))

def listaEventos(request):
    staff = False
    comunidad = False
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad:
            comunidad = True
        if cu.staff:
            staff = True
    except:
        pass

    for evento in Evento.objects.filter(cancelado=False, concluido=False):
        evento.cant_inscritos = 0
        for inscripcion in Inscripciones.objects.filter(evento=evento):
            evento.cant_inscritos = evento.cant_inscritos + inscripcion.cantidad
        if evento.cant_inscritos >= evento.cupos or evento.fecha_costo2 < date.today():
            evento.cerrado = True
        else:
            evento.cerrado = False

        if evento.fecha_costo1 > date.today():
            evento.costo = evento.costo1
            evento.fecha_costo = evento.fecha_costo1
        else:
            evento.costo = evento.costo2
            evento.fecha_costo = evento.fecha_costo2

        if evento.fecha < date.today():
            evento.concluido = True

        evento.save()
    return render(request, 'eventos/list.html', {
        'events': Evento.objects.filter(cancelado=False, concluido=False, prueba=False).order_by('fecha'),
        'all_events': Evento.objects.filter(cancelado=False, concluido=False).order_by('fecha'),
        'comunidad': comunidad,
        'staff': staff,
    })

@login_required
def agregarCupo(request, pk):
    event = Evento.objects.get(pk=pk)
    if event.cerrado:
        messages.success(request, 'Evento cerrado por cupos')
        return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))
        
    inscripcion = Inscripciones.objects.get(evento=event, usuario=request.user)
    inscripcion.cantidad = inscripcion.cantidad + 1
    inscripcion.save()
    return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))

@login_required
def quitarCupo(request, pk):
    event = Evento.objects.get(pk=pk)
    inscripcion = Inscripciones.objects.get(evento=event, usuario=request.user)
    if inscripcion.cantidad > 1:
        inscripcion.cantidad = inscripcion.cantidad - 1
        inscripcion.save()
        return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))
    
    messages.success(request, 'Solo tienes un cupo reservado')
    return HttpResponseRedirect(reverse("eventos.detail", args=(pk, )))