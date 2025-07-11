from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.dateparse import parse_date

from .models import Visit, MoneyMovement, VisitCalendar
from .forms import MovementFormSet


def actualizarVisita(visit):
    expenses = MoneyMovement.objects.filter(visit=visit)
    total_balance = 0
    fact_elec = 0
    for expense in expenses:
        if (
            expense.categoria == "venta_huevos"
            or expense.categoria == "venta_huerta"
            or expense.categoria == "otros_ingresos"
        ):
            total_balance += expense.valor
        else:
            if not expense.fact_elec:
                total_balance -= expense.valor
            else:
                fact_elec += expense.valor

    visit.total_balance = total_balance
    visit.facturas_elec = fact_elec
    visit.save()


@login_required
def listOfVisits(request):
    user = CustomUser.objects.get(user=request.user)

    comunidad = False
    if user.comunidad or user.staff or request.user.is_staff:
        visits = Visit.objects.all().order_by("-date")
        comunidad = True
    else:
        return HttpResponseRedirect(reverse("home"))

    return render(
        request,
        "visit/list.html",
        {
            "visits": visits,
            "comunidad": comunidad,
            "nickname": user.nickname,
        },
    )


@login_required
def visitDetails(request, pk):
    comunidad = False
    user = CustomUser.objects.get(user=request.user)
    if user.comunidad or user.staff or request.user.is_staff:
        visit = Visit.objects.get(pk=pk)
        comunidad = True
    else:
        return HttpResponseRedirect(reverse("home"))

    actualizarVisita(visit)
    expenses = MoneyMovement.objects.filter(visit=visit)
    return render(
        request,
        "visit/details.html",
        {
            "visit": visit,
            "expenses": expenses,
            "comunidad": comunidad,
            # 'message': message
        },
    )


@login_required
def visitInput(request):
    user = CustomUser.objects.get(user=request.user)
    if not user.comunidad and not user.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))

    if request.method == "POST":
        visitor = CustomUser.objects.get(user=request.user)
        date = parse_date(request.POST["date"])
        notes = request.POST["notes"]
        visitasCercanas = Visit.objects.filter(
            visitor=visitor,
            date__range=(
                date - timedelta(days=5),
                date + timedelta(days=5)
            )
        )
        
        if visitasCercanas.exists():
            return render(
                request,
                "visit/input.html",
                {
                    "comunidad": user.comunidad or user.staff or request.user.is_staff,
                    "nickname": user.nickname,
                    "staff": user.staff or request.user.is_staff,
                    "message": "Ya existe una visita para esa fecha, si necesitas modificarla, ve a la sección de visitas.",
                },
            )

        visit = Visit(visitor=visitor, date=date, notes=notes)
        visit.save()
        email = EmailMessage(
            "Nueva Visita",
            f"Nueva vista de {visitor.nickname.capitalize()} el {date}",
            settings.EMAIL_HOST_USER,
            [
                "juanfer_arango@hotmail.com",
                "quintanamagica@gmail.com",
            ],
        )
        email.fail_silently = False
        try:
            pass
            email.send()
        except:
            pass
        return redirect("visit.create_movement", pk=visit.id)

    return render(
        request,
        "visit/input.html",
        {
            "comunidad": user.comunidad or user.staff or request.user.is_staff,
            "nickname": user.nickname,
            "staff": user.staff or request.user.is_staff,
        },
    )


@login_required
def MovementInput(request, pk):
    user = request.user
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        if not cu.comunidad and not cu.staff and not request.user.is_staff:
            return HttpResponseRedirect(reverse("home"))
    except:
        return HttpResponseRedirect(reverse("home"))

    visit = Visit.objects.get(pk=pk)
    formset = MovementFormSet(request.POST or None)

    if request.method == "POST":
        if formset.is_valid():
            formset.instance = visit
            formset.save()
            return redirect("visit.details", pk=visit.id)

    context = {"formset": formset, "visit": visit, "comunidad": cu.comunidad or cu.staff or request.user.is_staff}

    return render(request, "visit/create_movement.html", context)


@login_required
def modificarVisita(request, pk):
    user = request.user
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        if not cu.comunidad and not cu.staff and not request.user.is_staff:
            return HttpResponseRedirect(reverse("home"))
    except:
        return HttpResponseRedirect(reverse("home"))
    visit = Visit.objects.get(pk=pk)
    fecha = f"{visit.date.year}-{visit.date.month:02d}-{visit.date.day:02d}"
    expenses = MoneyMovement.objects.filter(visit=visit)
    if request.method == "POST":
        try:
            visit.notes = request.POST["notes"]
        except:
            pass
        try:
            date = request.POST["date"]
            if date != "":
                visit.date = date
        except:
            visit.date = visit.date

        visit.save()
        return render(
            request,
            "visit/details.html",
            {
                "visit": visit,
                "expenses": expenses,
                "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                "fecha": fecha,
            },
        )
    else:
        message = None
        if cu != visit.visitor and not (cu.staff or request.user.is_staff):
            message = "Solo " + visit.visitor.nickname + " puede modificar esta visita"
            return render(
                request,
                "visit/details.html",
                {
                    "visit": visit,
                    "expenses": expenses,
                    "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                    "message": message,
                    "fecha": fecha,
                },
            )

        if visit.revisado and not (cu.staff or request.user.is_staff):
            message = "Visita ya revisada y asentanda"
            return render(
                request,
                "visit/details.html",
                {
                    "visit": visit,
                    "expenses": expenses,
                    "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                    "message": message,
                    "fecha": fecha,
                },
            )

        context = {
            "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
            "visit": visit,
            "expenses": expenses,
            "fecha": fecha,
        }
        return render(request, "visit/modify.html", context)


@login_required
def borrarMov(request, pk):
    mov = MoneyMovement.objects.get(pk=pk)
    visit = Visit.objects.get(id=mov.visit.id)
    if CustomUser.objects.get(user=request.user).user != visit.visitor.user and not CustomUser.objects.get(user=request.user).staff:
        return redirect("visit.details", pk=visit.id)
    
    mov.delete()
    actualizarVisita(visit)
    return redirect("visit.modify", pk=visit.id)


@login_required
def modificarMov(request, pk):
    mov = MoneyMovement.objects.get(pk=pk)
    visit = Visit.objects.get(id=mov.visit.id)
    if CustomUser.objects.get(user=request.user).user != visit.visitor.user and not CustomUser.objects.get(user=request.user).staff:
        return redirect("visit.details", pk=visit.id)
    
    valor = int(request.POST["valor"].replace(".", "").replace(",", ""))
    try:
        f = request.POST["factElec"]
    except:
        f = "no elec"
    
    mov.valor = valor
    if f == "elec":
        mov.fact_elec = True
    else:
        mov.fact_elec = False
    
    mov.save()
    actualizarVisita(visit)
    return redirect("visit.modify", pk=visit.id)


@login_required
def calendarOfVisits(request):
    user = CustomUser.objects.get(user=request.user)
    comunidad = False
    if user.comunidad or user.staff or request.user.is_staff:
        visits = VisitCalendar.objects.filter(
            date__range=[
                date.today() - timedelta(days=15),
                date.today() + timedelta(days=300),
            ]
        ).order_by("date")
        comunidad = True
    else:
        return HttpResponseRedirect(reverse("home"))

    return render(
        request,
        "visit/calendar.html",
        {
            "visits": visits,
            "comunidad": comunidad,
            "nickname": user.nickname,
            "staff": user.staff or request.user.is_staff,
        },
    )
    
@login_required
def EditCalendar(request, pk):
    visit = VisitCalendar.objects.get(pk=pk)
    user = CustomUser.objects.get(user=request.user)
    if not user.staff or not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    visitantes = CustomUser.objects.filter(visit_resp=True)
    if not user.comunidad and not user.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        visit.visitor = CustomUser.objects.get(user=User.objects.get(username=request.POST["visitante"]))
        visit.save()
        return HttpResponseRedirect(reverse("visit.calendar"))
    
    return render(
        request,
        "visit/edit_calendar.html",
        {
            "visit": visit,
            "visitantes": visitantes,
            "comunidad": user.comunidad or user.staff or request.user.is_staff,
        },
    )



@login_required
def myVisits(request):
    user = CustomUser.objects.get(user=request.user)
    comunidad = False
    if user.comunidad or user.staff or request.user.is_staff:
        visits = VisitCalendar.objects.filter(
            date__range=[
                date.today() - timedelta(days=15),
                date.today() + timedelta(days=300),
            ],
            visitor=user,
        ).order_by("date")
        comunidad = True
    else:
        return HttpResponseRedirect(reverse("home"))

    return render(
        request,
        "visit/myvisits.html",
        {
            "visits": visits,
            "comunidad": comunidad,
            "nickname": user.nickname,
        },
    )


@login_required
def datosContabilidad(request):
    user = CustomUser.objects.get(user=request.user)
    if not user.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        visita = request.POST["visita"]
        revisado = request.POST.get("revisado", False)
        if revisado == "on":
            visit = Visit.objects.get(id=visita)
            visit.revisado = True
            visit.save()
    
    class visitasSinRevisar():
        def __init__(self, user, saldoEfectivo, saldoFactElec, fecha, key):
            self.user = user
            self.fecha = fecha
            self.saldoEfectivo = saldoEfectivo
            self.saldoFactElec = saldoFactElec
            self.key = key
    
    visitas = []
    movimientos = {}
    for visita in Visit.objects.filter(revisado=False):
        visitas.append(visitasSinRevisar(
            visita.visitor.nickname,
            visita.total_balance,
            visita.facturas_elec,
            visita.date,
            visita.id
        ))
        for movimiento in MoneyMovement.objects.filter(visit=visita):
            if not movimiento.fact_elec:
                try:
                    movimientos[movimiento.categoria] += movimiento.valor
                except:
                    movimientos[movimiento.categoria] = movimiento.valor

    return render(request, "visit/datos_contabilidad.html",
                  {
                      "comunidad": user.comunidad or user.staff or request.user.is_staff,
                      "visitas": visitas,
                      "movimientos": movimientos,
                      "staff": user.staff or request.user.is_staff,
                  })

    
@login_required
def eliminarVisita(request, pk):
    user = request.user
    try:
        cu = CustomUser.objects.get(user_id=user.id)
        if not cu.comunidad and not cu.staff and not request.user.is_staff:
            return HttpResponseRedirect(reverse("home"))
    except:
        return HttpResponseRedirect(reverse("home"))
    visit = Visit.objects.get(pk=pk)
    expenses = MoneyMovement.objects.filter(visit=visit)
    if request.method == "POST":
        visit.save()
        for expense in expenses:
            expense.delete()
        visit.delete()
        return HttpResponseRedirect(reverse("visit.list"))
    else:
        return HttpResponseRedirect(reverse("home"))