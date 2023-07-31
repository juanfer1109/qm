from celery import shared_task
from datetime import date
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Inscripciones, Evento
from users.models import CustomUser


@shared_task(bind=True)
def RecordarPago(token):
    inscritos_sin_pago = Inscripciones.objects.filter(pago_recibido=False)
    for inscrito in inscritos_sin_pago:
        usuario = CustomUser.objects.get(user=inscrito.usuario)
        evento = Evento.objects.get(id=inscrito.evento.id)
        subject = "Inscripción en el evento " + evento.nombre
        template = get_template("eventos/email_recorderis.html")
        content = template.render(
            {
                "usuario": usuario,
                "cantidad": inscrito.cantidad,
                "evento": evento,
            }
        )
        sendTo = User.objects.get(username=inscrito.usuario).email
        bcc_email = "quintanamagica@gmail.com"
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


@shared_task(bind=True)
def PromocionarEventos(token):
    talleres = Evento.objects.filter(
        cancelado=False, concluido=False, cerrado=False, prueba=False
    )
    if len(talleres) > 0:
        lista_correo = CustomUser.objects.filter(mailing_list=True, comunidad=False)

        for taller in talleres:
            subject = "Invitación al evento " + taller.nombre
            inscritos = []
            for inscrito in Inscripciones.objects.filter(evento=taller):
                inscritos.append(inscrito.usuario)
            for persona in lista_correo:
                if User.objects.get(customuser=persona) not in inscritos:
                    template = get_template("eventos/email_invitacion_evento.html")
                    content = template.render(
                        {
                            "usuario": persona,
                            "evento": taller,
                        }
                    )
                    sendTo = User.objects.get(username=persona.user).email
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


@shared_task(bind=True)
def ActualizarInscripciones(token):
    eventos = Evento.objects.filter(concluido=False, cancelado=False)
    for evento in eventos:
        inscripciones = Inscripciones.objects.filter(evento=evento)
        for inscripcion in inscripciones:
            inscripcion.valor_total = (
                inscripcion.cantidad * inscripcion.valor_segun_fecha
            )
            if inscripcion.valor_recibido == inscripcion.valor_total:
                inscripcion.pago_recibido = True
            else:
                inscripcion.pago_recibido = False
            inscripcion.save()
