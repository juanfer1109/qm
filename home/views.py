from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime as dt
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'home/welcome.html'
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
    # user = User.objects.get(username=)
    # username = user.username
    # user = CustomUser.objects.get(user=username)
    gender = 'Juanfer'
    mes = meses.get(dt.today().month)
    fecha = str(dt.today().day) + " de " + mes + " de " + str(dt.today().year)
    extra_context = {'today': fecha, 'gender': gender}

