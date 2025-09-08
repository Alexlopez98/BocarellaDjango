from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil
from .models import Pizza, Promocion, Acompanamiento, Extra

def home(request):
    return render(request, "index.html")

def home(request):
    carousel = [
        {"id": "DUOPEPPE", "img": "img/DUOPEPPE.png"},
        {"id": "PIZZADUO", "img": "img/PIZZADUO.jpg"},
        {"id": "PIZZAGAMER", "img": "img/PIZZAGAMER.png"},
    ]
    return render(request, "index.html", {"carousel": carousel})

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


@login_required
def perfil(request):
    user = request.user
    perfil, created = Perfil.objects.get_or_create(user=user)

    if request.method == "POST":
        nombre = request.POST.get("perfilNombre").strip()
        email = request.POST.get("perfilEmail").strip()
        direccion = request.POST.get("perfilDireccion").strip()
        password = request.POST.get("perfilPass")
        confirm = request.POST.get("perfilConfirm")

        if nombre and email and direccion:
            user.first_name = nombre
            user.email = email
            perfil.direccion = direccion

            if password:
                if password == confirm:
                    user.set_password(password)
                else:
                    messages.error(request, "❌ Las contraseñas no coinciden.")
                    return redirect("perfil")

            user.save()
            perfil.save()
            messages.success(request, "✅ Perfil actualizado correctamente.")
            return redirect("perfil")
        else:
            messages.error(request, "❌ Todos los campos son obligatorios.")
            return redirect("perfil")

    context = {
        "user": user,
        "perfil": perfil
    }
    return render(request, "perfil.html", context)

def pizzas(request):
    pizzas = [
        {
            "id": 1,
            "nombre": "Pizza Margarita",
            "descripcion": "Clásica con tomate, mozzarella y albahaca.",
            "precio": 7990,
            "imagen": "img/margarita.jpeg",
        },
        {
            "id": 2,
            "nombre": "Pizza Pepperoni",
            "descripcion": "Mozzarella y abundante pepperoni.",
            "precio": 8990,
            "imagen": "img/pepperoni.jpeg",
        },
        {
            "id": 3,
            "nombre": "Pizza Vegetariana",
            "descripcion": "Con champiñones, pimientos y aceitunas.",
            "precio": 8490,
            "imagen": "img/hawaiana.avif",
        },
    ]
    return render(request, "pizzas.html", {"pizzas": pizzas})

def promociones(request):
    promos = [
        {
            "id": 1,
            "titulo": "Promo Duo Bocarella",
            "descripcion": "2 pizzas medianas + bebida",
            "precio": 15990,
            "imagen": "img/DUOPEPPE.png"
        },
        {
            "id": 2,
            "titulo": "Promo Gamer",
            "descripcion": "1 pizza gamer + bebida + postre",
            "precio": 12990,
            "imagen": "img/PIZZAGAMER.png"
        },
        {
            "id": 3,
            "titulo": "Pizza Duo",
            "descripcion": "2 pizzas grandes al mejor precio",
            "precio": 17990,
            "imagen": "img/PIZZADUO.jpg"
        }
    ]

    return render(request, "promociones.html", {"promos": promos})

def acompanamientos(request):
    acompanamientos = [
        {
            "id": 1,
            "nombre": "Tiramisu",
            "precio": 1490,
            "imagen": "tiramisu.webp"
        },
        {
            "id": 2,
            "nombre": "Cheescake",
            "precio": 990,
            "imagen": "cheesecakefrutilla.webp"
        },
        {
            "id": 3,
            "nombre": "Papas Fritas",
            "precio": 2990,
            "imagen": "img/papasfritas.jpg"
        }
    ]

    return render(request, "acompanamientos.html", {"acompanamientos": acompanamientos})

def extras(request):
    extras = [
        {
            "id": 1,
            "nombre": "Helado de Vainilla",
            "precio": 1990,
            "imagen": "img/helado_vainilla.png"
        },
        {
            "id": 2,
            "nombre": "Brownie",
            "precio": 2490,
            "imagen": "img/brownie.png"
        },
        {
            "id": 3,
            "nombre": "Cheesecake",
            "precio": 2990,
            "imagen": "img/cheesecake.png"
        }
    ]
    return render(request, "extras.html", {"extras": extras})