from django.urls import path

from . import views
from home import views as vw

urlpatterns = [
    path('', vw.homeView),
    path('-login', views.LoginInterfaceView.as_view(), name='users.login'),
    path('-signup', views.SignUp, name='users.signup'),
    path('-logout', views.LogoutInterfaceView.as_view(), name='users.logout'),
    path('-profile', views.MyProfile, name='users.profile'),
]