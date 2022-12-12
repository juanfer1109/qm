from django.urls import path

from . import views

urlpatterns = [
    path('-login', views.LoginInterfaceView.as_view(), name='users.login'),
    path('-signup', views.SignupView.as_view(), name='users.signup'),
    path('-logout', views.LogoutInterfaceView.as_view(), name='users.logout'),
]