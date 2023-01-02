from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime as dt
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import NewUserForm, NewUserForm2
from .models import CustomUser

class SignupView(CreateView):
    form_class = NewUserForm
    # form_class = NewUserForm2
    template_name = 'users/register.html'
    success_url = '/login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

class LogoutInterfaceView(LogoutView):
    message = "Te esperamos pronto"
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
    mes = meses.get(dt.today().month)
    fecha = str(dt.today().day) + " de " + mes + " de " + str(dt.today().year)
    extra_context = {'message': message, 'today':fecha}
    template_name = 'home/welcome.html'


class LoginInterfaceView(LoginView):
    template_name = 'users/login.html'

def SignUp(request):
    if request.method == 'POST':
        ok = False
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        birthday = request.POST["birthday"]
        nickname = request.POST["nickname"]
        try:
            if  int(phone_number) >= 3000000000 and int(phone_number) <= 3999999999:
                pass
            else:
                ok = True
                message = "Número de celular invalido"
        except:
            ok = True
            message = "Número de celular invalido"

        try:
            date = dt.strptime(birthday, '%Y-%m-%d')
        except:
            ok = True
            message = "Fecha invalida"

        try:
            if request.POST["mailing_list"] == 'True':
                mailing_list = True
        except:
            mailing_list = False
            
        if request.POST["info_manage"] == "True":
            info_manage = True
        else:
            info_manage = False


        password = request.POST["password"]
        confirmation = request.POST["password2"]
        if password != confirmation:
            ok = True
            message = "Las contraseñas deben coincidir"

        if not ok:
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                customUser = CustomUser(user_id=user.id, birthday=birthday, phone_number=phone_number)
                customUser.mailing_list = mailing_list
                customUser.info_manage = info_manage
                customUser.nickname = nickname
            except IntegrityError:
                ok = True
                message = "Usuario ya existe"

        if not ok:
            customUser.save()
            user.save()
        else:
            return render(request, "users/signup.html", {
                "message": message,
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "birthday": birthday,
                "nickname": nickname,
            })

        login(request, user)
        return HttpResponseRedirect(reverse("home"))

    return render(request, 'users/signup.html')

def MyProfile(request):
    actual_user = User.objects.get(username=request.user)
    actual_cu = CustomUser.objects.get(user=request.user)
    a_username = actual_user.username
    a_email = actual_user.email
    a_first_name = actual_user.first_name
    a_last_name = actual_user.last_name
    a_phone_number = actual_cu.phone_number
    a_birthday = actual_cu.birthday
    a_nickname = actual_cu.nickname
    a_mailing_list = actual_cu.mailing_list
    a_password = actual_user.password
    if request.method == 'POST':
        ok = False
        # username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        try:
            if  int(phone_number) >= 3000000000 and int(phone_number) <= 3999999999:
                pass
            else:
                ok = True
                message = "Número de celular invalido"
        except:
            ok = True
            message = "Número de celular invalido"

        # birthday = request.POST["birthday"]
        nickname = request.POST["nickname"]
        try:
            if request.POST["mailing_list"] == 'True':
                mailing_list = True
        except:
            mailing_list = False

        if not ok:
            # actual_user.username = username
            actual_user.email = email
            actual_user.first_name = first_name
            actual_user.last_name = last_name
            actual_cu.phone_number = phone_number
            actual_cu.nickname = nickname
            actual_cu.mailing_list = mailing_list
            actual_user.save()
            actual_cu.save()

            login(request, actual_user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, 'users/profile.html', {
                'a_username': a_username,
                'a_email': a_email,
                'a_first_name': a_first_name,
                'a_last_name': a_last_name,
                # 'a_birthday': a_birthday,
                'a_mailing_list': a_mailing_list,
                'a_phone_number': a_phone_number,
                'a_nickname': a_nickname,
                'message': message,

            })

    return render(request, 'users/profile.html', {
        'a_username': a_username,
        'a_email': a_email,
        'a_first_name': a_first_name,
        'a_last_name': a_last_name,
        # 'a_birthday': a_birthday,
        'a_mailing_list': a_mailing_list,
        'a_phone_number': a_phone_number,
        'a_nickname': a_nickname,

    })