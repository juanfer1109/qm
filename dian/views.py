from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import DianDoc
from users.models import CustomUser

def docsDian(request):
    comunidad = False
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad == True:
            comunidad =True
    except:
        pass

    listOfYears = DianDoc.objects.values_list('year', flat=True).distinct()
    listOfYears.order_by('year').reverse()
    
    if request.method == 'POST':
        year = request.POST['year']
        listOfDocs = DianDoc.objects.filter(year=year)
        list = True
        if len(listOfDocs) == 0:
            list = False

        return render(request, 'dian/docs.html', {
            'list': list,
            'documents' : listOfDocs,
            'years': listOfYears,
            'comunidad': comunidad,
        })

    return render(request, 'dian/docs.html', {
        'years': listOfYears,
        'comunidad': comunidad,
    })


def pdfOpen(request, pk):
    doc = DianDoc.objects.get(pk=pk)
    return render(request, 'dian/pdf.html', {
        'pdf': doc,
    })
