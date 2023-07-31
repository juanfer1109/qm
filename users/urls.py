from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


from . import views
from home import views as vw

urlpatterns = [
    path("", vw.homeView),
    path("login/", views.LogIn, name="users.login"),
    path("signup/", views.SignUp, name="users.signup"),
    path("logout/", views.LogoutInterfaceView.as_view(), name="users.logout"),
    path("profile/", views.MyProfile, name="users.profile"),
    path("passchange/", views.cambiarPassword, name="users.change_password"),
    path(
        "resetpass/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
