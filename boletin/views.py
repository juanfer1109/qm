from django.shortcuts import render
from datetime import date

from .models import Issue, Article

def listOfIssues(request, ed):
    boletin = Issue.objects.get(ed=ed)
    return render(request, 'boletin/boletin.html', {
        'fecha':  date.today(),
        'boletin': boletin,
    })
