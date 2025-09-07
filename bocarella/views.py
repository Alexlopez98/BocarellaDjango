from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



def home(request):
    return render(request, 'index.html')  

def home(request):
    carousel = [
        {"id": "DUOPEPPE", "img": "img/DUOPEPPE.png"},
        {"id": "DUOPEPPE2", "img": "img/SUPERDUO.png"},
        {"id": "DUOPEPPE3", "img": "img/PIZZAGAMER.png"},
    ]
    return render(request, 'index.html', {"carousel": carousel})


def acceso(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "❌ Usuario no encontrado.")
            return redirect("acceso")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"✅ Bienvenido {user.username}")
            return redirect("index")
        else:
            messages.error(request, "❌ Contraseña incorrecta.")
    return render(request, "acceso.html")

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        usuario = request.POST.get("usuario")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=usuario).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "❌ Usuario o correo ya registrado.")
            return redirect("registro")
        user = User.objects.create_user(username=usuario, email=email, password=password, first_name=nombre)
        messages.success(request, "✅ Registro exitoso. Ya puedes iniciar sesión.")
        return redirect("acceso")
    return render(request, "registro.html")

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "👋 Sesión cerrada.")
    return redirect("index")