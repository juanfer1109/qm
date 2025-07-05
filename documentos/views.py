from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import CustomUser
from .models import TipoDocumento, Documento
from .forms import TipoForm, DocumentoForm


@login_required
def listaDocumentos(request):
    cu = CustomUser.objects.get(user=request.user)
    if not cu.comunidad and not cu.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        try:
            tipo = request.POST["tipo"]
        except:
            print("No se ha seleccionado ningún tipo de documento.")
            
            return render(
                request,
                "documentos/list.html",
                {
                    "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                    "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
                    "get": True,
                    "staff": cu.staff or request.user.is_staff,
                    "message": "No se ha seleccionado ningún tipo de documento.",
                },
            )
            
        return render(
            request,
            "documentos/list.html",
            {
                "list": len(Documento.objects.filter(tipo=tipo)) > 0,
                "documents": Documento.objects.filter(tipo=tipo).order_by("-date"),
                "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
                "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                "tipo_consulta": TipoDocumento.objects.get(id=tipo).id,
                "staff": cu.staff or request.user.is_staff,
            },
        )
    
    return render(
        request,
        "documentos/list.html",
        {
            "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
            "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
            "get": True,
            "staff": cu.staff or request.user.is_staff,
        },
    )
    

@login_required
def nuevoTipo(request):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        form = TipoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except:
                return render(request, "documentos/formulario_tipo.html", {
                "form": form, 
                "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
                "staff": cu.staff or request.user.is_staff,
                })
        else:
            return render(request, "documentos/formulario_tipo.html", {
                "form": form, 
                "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
                "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
                "staff": cu.staff or request.user.is_staff,
                })
    
    form = TipoForm()
    return render(request, "documentos/formulario_tipo.html", {
        "form": form, 
        "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
        "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
        "staff": cu.staff or request.user.is_staff,
        })
    
@login_required
def borrarTipo(request, pk):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    tipo = TipoDocumento.objects.get(id=pk)
    
    if len(Documento.objects.filter(tipo=tipo)) == 0:
        tipo.delete()
    else:
        mensaje = "No se puede eliminar el tipo de documento porque ya hay documentos asociados a este tipo."
        return render(request, "documentos/formulario_tipo.html", {
            "form": TipoForm(), 
            "comunidad": cu.comunidad or cu.staff or request.user.is_staff,
            "tipos": TipoDocumento.objects.all().order_by("tipo").values(),
            "message": mensaje,
            "staff": cu.staff or request.user.is_staff,
            })
    
    return HttpResponseRedirect(reverse("documentos.nuevotipo"))


@login_required
def borrarDocumento(request, pk):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    Documento.objects.get(id=pk).delete()
    
    return HttpResponseRedirect(reverse("documentos.list"))


@login_required
def nuevoDoc(request):
    user = request.user
    cu = CustomUser.objects.get(user=user)
    if not cu.comunidad and not cu.staff and not request.user.is_staff:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = cu
            form.save()
        else:
            return render(request, "documentos/crear_documento.html", {"form": form, "comunidad": cu.comunidad or cu.staff or request.user.is_staff,})
    
    form = DocumentoForm()
    return render(request, "documentos/crear_documento.html", {"form": form, "comunidad": cu.comunidad or cu.staff or request.user.is_staff,})