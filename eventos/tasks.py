from celery import shared_task
from datetime import date
from django.template.loader import get_template
from django.contrib. auth.models import User
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
        subject = 'Estas inscrito en el evento ' + evento.nombre
        template = get_template('eventos/email_recorderis.html')
        content = template.render({
            'usuario': usuario,
            'cantidad': inscrito.cantidad,
            'evento': evento,
        })
        sendTo = User.objects.get(username=inscrito.usuario).email
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