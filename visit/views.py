from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import date, timedelta

from .models import Visit, MoneyMovement, VisitCalendar
from .forms import MovementFormSet

@login_required
def listOfVisits(request):
    user = CustomUser.objects.get(user=request.user)

    comunidad = False
    if user.comunidad == True:
        visits = Visit.objects.all().order_by('-date')
        comunidad =True
    else:
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'visit/list.html', {
        'visits': visits,
        'comunidad': comunidad,
        'nickname': user.nickname,
    })

@login_required
def visitDetails(request, pk):
    comunidad = False
    user = CustomUser.objects.get(user=request.user)
    if user.comunidad == True:
        visit = Visit.objects.get(pk=pk)
        comunidad = True
    else:
        return HttpResponseRedirect(reverse('home'))

    expenses = MoneyMovement.objects.filter(visit=visit)

    total_balance = 0
    for expense in expenses:
        if expense.categoria == 'venta_huevos' or expense.categoria == 'venta_huerta' or expense.categoria == 'otros_ingresos':
            total_balance += expense.valor
        else:
            total_balance -= expense.valor

    visit.total_balance = total_balance
    visit.save()
    
    return render(request, 'visit/details.html', {
        'visit': visit,
        'expenses': expenses,
        'comunidad': comunidad,
        # 'message': message
    })

@login_required
def visitInput(request):
    comunidad = False
    user = CustomUser.objects.get(user=request.user)
    if user.comunidad == False:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        visitor = CustomUser.objects.get(user=request.user)
        date = request.POST["date"]
        notes = request.POST["notes"]
        visit = Visit(visitor=visitor, date=date, notes=notes)
        visit.save()
        return redirect('visit.create_movement', pk=visit.id)


    return render(request, 'visit/input.html', {
        'comunidad': user.comunidad,
        'nickname': user.nickname,
    })

@login_required
def MovementInput(request, pk):
    user = request.user
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad == False:
            return HttpResponseRedirect(reverse('home'))
    except:
        return HttpResponseRedirect(reverse('home'))

    visit = Visit.objects.get(pk=pk)
    formset = MovementFormSet(request.POST or None)

    if request.method == 'POST':
        if formset.is_valid():
            formset.instance = visit
            formset.save()
            return redirect('visit.details', pk=visit.id)

    context = {
        'formset': formset,
        'visit': visit,
        'comunidad': cu.comunidad
    }

    return render(request, 'visit/create_movement.html', context)

@login_required
def modificarVisita(request, pk):
    user = request.user
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad == False:
            return HttpResponseRedirect(reverse('home'))
    except:
        return HttpResponseRedirect(reverse('home'))
    visit = Visit.objects.get(pk=pk)
    expenses = MoneyMovement.objects.filter(visit=visit)
    if request.method == 'POST':
        try:
            visit.notes = request.POST['notes']
        except:
            pass
        try:
            date = request.POST['date']
            if date !='':
                visit.date = date
        except:
            visit.date = visit.date

        visit.save()
        return render(request, 'visit/details.html', {
                'visit': visit,
                'expenses': expenses,
                'comunidad': cu.comunidad,
            })
    else:
        message = None
        if cu != visit.visitor:
            message = 'Solo ' + visit.visitor.nickname + ' puede modificar esta visita'
            return render(request, 'visit/details.html', {
                'visit': visit,
                'expenses': expenses,
                'comunidad': cu.comunidad,
                'message': message
            })
        
        if visit.revisado:
            message = 'Visita ya revisada y asentanda'
            return render(request, 'visit/details.html', {
                'visit': visit,
                'expenses': expenses,
                'comunidad': cu.comunidad,
                'message': message
            })

        context = {
            'comunidad': cu.comunidad,
            'visit': visit,
            'expenses': expenses,
        }
        return render(request, 'visit/modify.html', context)

@login_required
def borrarMov(request, pk):
    mov = MoneyMovement.objects.get(pk=pk)
    visit = Visit.objects.get(id=mov.visit.id)
    if CustomUser.objects.get(user=request.user).user != visit.visitor.user:
        return redirect('visit.details', pk=visit.id)

    if mov.categoria == 'venta_huevos' or mov.categoria == 'venta_huerta' or mov.categoria == 'otros_ingresos':
        visit.total_balance = visit.total_balance - mov.valor
    else:
        visit.total_balance = visit.total_balance + mov.valor

    visit.save()
    mov.delete()
    return redirect('visit.modify', pk=visit.id)

@login_required
def modificarMov(request, pk):
    valor = int(request.POST['valor'].replace('.', '').replace(',', ''))
    mov = MoneyMovement.objects.get(pk=pk)
    visit = Visit.objects.get(id=mov.visit.id)
    if CustomUser.objects.get(user=request.user).user != visit.visitor.user:
        return redirect('visit.details', pk=visit.id)

    if mov.categoria == 'venta_huevos' or mov.categoria == 'venta_huerta' or mov.categoria == 'otros_ingresos':
        visit.total_balance = visit.total_balance - mov.valor + valor
    else:
        visit.total_balance = visit.total_balance + mov.valor - valor

    visit.save()
    mov.valor = valor
    mov.save()
    return redirect('visit.modify', pk=visit.id)

@login_required
def calendarOfVisits(request):
    user = CustomUser.objects.get(user=request.user)
    comunidad = False
    if user.comunidad == True:
        visits = VisitCalendar.objects.filter(date__range=[date.today() 
                                        - timedelta(days=15), date.today() + timedelta(days=300)]).order_by('date')
        comunidad =True
    else:
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'visit/calendar.html', {
        'visits': visits,
        'comunidad': comunidad,
        'nickname': user.nickname,
    })

@login_required
def myVisits(request):
    user = CustomUser.objects.get(user=request.user)
    comunidad = False
    if user.comunidad == True:
        visits = VisitCalendar.objects.filter(date__range=[date.today() 
                                        - timedelta(days=30), date.today() + timedelta(days=300)], visitor=user).order_by('date')
        comunidad =True
    else:
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'visit/myvisits.html', {
        'visits': visits,
        'comunidad': comunidad,
        'nickname': user.nickname,
    })