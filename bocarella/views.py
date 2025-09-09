from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
#from .models import Perfil

# ------------------------------
# HOME
# ------------------------------
def home(request):
    carousel = [
        {"id": "DUOPEPPE", "img": "img/DUOPEPPE.png"},
        {"id": "PIZZADUO", "img": "img/PIZZADUO.jpg"},
        {"id": "PIZZAGAMER", "img": "img/PIZZAGAMER.png"},
    ]
    return render(request, "index.html", {"carousel": carousel})

# ------------------------------
# ACCESO / REGISTRO / CERRAR SESIÓN
# ------------------------------
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

# ------------------------------
# PERFIL
# ------------------------------
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

    context = {"user": user, "perfil": perfil}
    return render(request, "perfil.html", context)

# ------------------------------
# PRODUCTOS EN MEMORIA
# ------------------------------
PRODUCTOS = [
    # Pizzas
    {"id": 1, "nombre": "Margarita", "descripcion": "Pizza clásica con tomate y queso", "precio": 7990, "imagen": "img/margarita.jpeg", "categoria": "pizza"},
    {"id": 2, "nombre": "Pepperoni", "descripcion": "Pizza con pepperoni y queso", "precio": 8990, "imagen": "img/pepperoni.jpeg", "categoria": "pizza"},
    {"id": 3, "nombre": "hawaiana", "descripcion": "pizza con piña y queso", "precio": 8490, "imagen": "img/hawaiana.avif", "categoria": "pizza"},

    # Promociones
    {"id": 10, "nombre": "Promo Duo Bocarella", "descripcion": "2 pizzas medianas + bebida", "precio": 15990, "imagen": "img/duopepe.png", "categoria": "promocion"},
    {"id": 11, "nombre": "Promo Gamer", "descripcion": "1 pizza gamer + bebida + postre", "precio": 12990, "imagen": "img/pizzagamer.jpg", "categoria": "promocion"},
    {"id": 12, "nombre": "Pizza Duo", "descripcion": "2 pizzas grandes al mejor precio", "precio": 17990, "imagen": "img/pizzaduo.jpg", "categoria": "promocion"},

    # Acompañamientos
    {"id": 20, "nombre": "Tiramisu", "precio": 1490, "imagen": "img/tiramisu.webp", "categoria": "acompanamiento"},
    {"id": 21, "nombre": "Alitas de pollo", "precio": 990, "imagen": "img/alitaspollo.avif", "categoria": "acompanamiento"},
    {"id": 22, "nombre": "Papas fritas", "precio": 2990, "imagen": "img/papasfritas.jpg", "categoria": "acompanamiento"},

    # Extras
    {"id": 30, "nombre": "Bebidas en lata", "precio": 1990, "imagen": "img/bebidas.jpg", "categoria": "extra"},
    {"id": 31, "nombre": "Brownie", "precio": 2490, "imagen": "img/browniehelado.png", "categoria": "extra"},
    {"id": 32, "nombre": "Cheesecake", "precio": 2990, "imagen": "img/cheesecakefrutilla.webp", "categoria": "extra"},
]

# ------------------------------
# VISTAS DE CATEGORÍAS
# ------------------------------
def pizzas(request):
    productos = [p for p in PRODUCTOS if p['categoria'] == 'pizza']
    return render(request, 'pizzas.html', {'pizzas': productos})

def promociones(request):
    productos = [p for p in PRODUCTOS if p['categoria'] == 'promocion']
    return render(request, 'promociones.html', {'promos': productos})

def acompanamientos(request):
    productos = [p for p in PRODUCTOS if p['categoria'] == 'acompanamiento']
    return render(request, 'acompanamientos.html', {'acompanamientos': productos})

def extras(request):
    productos = [p for p in PRODUCTOS if p['categoria'] == 'extra']
    return render(request, 'extras.html', {'extras': productos})

# ------------------------------
# CARRITO
# ------------------------------
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for producto_id_str, cantidad in carrito.items():
        producto_id = int(producto_id_str)
        producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
        if producto:
            item_total = producto['precio'] * cantidad
            total += item_total
            items.append({'producto': producto, 'cantidad': cantidad, 'total': item_total})
    return render(request, 'carrito.html', {'carrito': {'items': items, 'total': total}})

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('carrito')

def checkout(request):
    request.session['carrito'] = {}
    return redirect('index') 
