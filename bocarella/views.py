from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil
from .forms import RegistroForm, PerfilForm

# ------------------------------
# HOME
# ------------------------------
def home(request):
    carousel = [
        {"id": "DUOPEPPE", "img": "img/duopepe.png"},
        {"id": "PIZZADUO", "img": "img/pizzaduo.jpg"},
        {"id": "PIZZAGAMER", "img": "img/pizzagamer.jpg"},
    ]
    return render(request, "index.html", {"carousel": carousel})

# ------------------------------
# Registro de usuario
# ------------------------------
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Crear perfil con rol por defecto 'user'
            Perfil.objects.create(user=user, rol='user')
            login(request, user)
            messages.success(request, f"✅ Bienvenido {user.username}")
            return redirect('index')  # redirige al inicio
        else:
            messages.error(request, "❌ Corrige los errores del formulario")
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


# ------------------------------
# Login
# ------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            # Redirigir según rol
            if hasattr(user, 'perfil') and user.perfil.rol == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'login.html')


# ------------------------------
# Logout
# ------------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "👋 Has cerrado sesión correctamente")
    return redirect('index')


# ------------------------------
# Perfil de usuario
# ------------------------------
@login_required
def perfil_view(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            # Actualizar nombre y apellido del usuario
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.save()
            
            messages.success(request, "Perfil actualizado correctamente")
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'perfil.html', {'form': form})


# ------------------------------
# Dashboard de administrador
# ------------------------------
@login_required
def admin_dashboard(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'admin':
        messages.warning(request, "No tienes permisos de administrador")
        return redirect('index')
    return render(request, 'admin_dashboard.html')

# ------------------------------
# PRODUCTOS EN MEMORIA
# ------------------------------
PRODUCTOS = [
    # Pizzas
    {"id": 1, "nombre": "MARGARITA", "descripcion": "Pizza clásica con tomate y queso", "precio": 7990, "imagen": "img/margarita.jpeg", "categoria": "pizza"},
    {"id": 2, "nombre": "PEPPERONI", "descripcion": "Pizza con pepperoni y queso", "precio": 8990, "imagen": "img/pepperoni.jpeg", "categoria": "pizza"},
    {"id": 3, "nombre": "HAWAIANA", "descripcion": "Pizza con piña y queso", "precio": 8490, "imagen": "img/hawaiana.avif", "categoria": "pizza"},

    # Promociones
    {"id": 10, "nombre": "Promo Duo Bocarella", "descripcion": "2 Pizzas medianas + bebida", "precio": 15990, "imagen": "img/duopepe.png", "categoria": "promocion"},
    {"id": 11, "nombre": "Promo Gamer", "descripcion": "1 Pizza gamer + bebida + postre", "precio": 12990, "imagen": "img/pizzagamer.jpg", "categoria": "promocion"},
    {"id": 12, "nombre": "Pizza Duo", "descripcion": "2 Pizzas grandes al mejor precio", "precio": 17990, "imagen": "img/pizzaduo.jpg", "categoria": "promocion"},

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
