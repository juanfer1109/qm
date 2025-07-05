from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import DIANForm
from .models import DianDoc
from users.models import CustomUser



def docsDian(request):
    comunidad = False
    try:
        user = request.user
        cu = CustomUser.objects.get(user_id=user.id)
        if cu.comunidad or cu.staff or request.user.is_staff:
            comunidad = True
    except:
        pass

    listOfYears = DianDoc.objects.values_list("year", flat=True).distinct()
    listOfYears = listOfYears.order_by("year").reverse()

    if request.method == "POST":
        year = int(request.POST["year"].replace(".", "").replace(",", ""))
        listOfDocs = DianDoc.objects.filter(year=year)
        list = True
        if len(listOfDocs) == 0:
            list = False

        return render(
            request,
            "dian/docs.html",
            {
                "list": list,
                "documents": listOfDocs,
                "years": listOfYears,
                "comunidad": comunidad,
            },
        )

    return render(
        request,
        "dian/docs.html",
        {
            "years": listOfYears,
            "comunidad": comunidad,
        },
    )

# def handle_uploaded_file(f):
#     with open("some/file/name.txt", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# @login_required
# def nuevoDoc(request):
#     user = request.user
#     cu = CustomUser.objects.get(user=user)
#     if not cu.staff and not request.user.is_staff:
#         return HttpResponseRedirect(reverse("home"))
    
#     if request.method =='POST':
#         year = request.POST["year"]                
#         titulo = request.POST["titulo"]
#         nombre_file = 'dian-docs/' + request.POST["file"]
#         file = request.FILES["file"]
#         doc = DianDoc(year=year, title=titulo, file=nombre_file)
#         doc.save()
#         return render(
#         request,
#         'dian/form_registro.html',
#         {
#             "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
#             "message1": "Documento agregado",
#         }
#     )
    
#     return render(
#         request,
#         'dian/form_registro.html',
#         {
#             "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
#         }
#     )
    
@login_required
def nuevoDoc(request):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        form = DIANForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request, "dian/form_registro.html", {"form": form, "comunidad": cu.comunidad or cu.staff or request.user.is_staff,})
    
    form = DIANForm()
    return render(request, "dian/form_registro.html", {"form": form, "comunidad": cu.comunidad or cu.staff or request.user.is_staff,})