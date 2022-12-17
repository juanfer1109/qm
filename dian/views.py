from django.shortcuts import render

from .models import DianDoc

def docsDian(request):
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
        })

    return render(request, 'dian/docs.html', {
        'years': listOfYears,
    })

def pdfOpen(request, pk):
    doc = DianDoc.objects.get(pk=pk)
    return render(request, 'dian/pdf.html', {
        'pdf': doc,
    })
