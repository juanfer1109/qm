from django.urls import path
from . import views

urlpatterns = [
    path('issue/<int:ed>', views.listOfIssues, name="list_issues"),
]
