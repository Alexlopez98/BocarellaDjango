from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, Pizza, Promocion, Acompanamiento, Extra, Orden, OrdenItem
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
            Perfil.objects.create(user=user, rol='usuario')
            login(request, user)
            messages.success(request, f"✅ Bienvenido {user.username}")
            return redirect('index')
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
            if hasattr(user, 'perfil') and user.perfil.rol == 'admin':
                return redirect('admin_dashboard')
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
# CARRITO
# ------------------------------
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for producto_id, cantidad in carrito.items():
        # Buscamos en todos los modelos
        producto = None
        for modelo in [Pizza, Promocion, Acompanamiento, Extra]:
            try:
                producto = modelo.objects.get(id=producto_id)
                break
            except modelo.DoesNotExist:
                continue
        if producto:
            subtotal = producto.precio * cantidad
            total += subtotal
            items.append({
                "producto": producto,
                "cantidad": cantidad,
                "total": subtotal,
            })
    contexto = {"carrito": {"items": items, "total": total}}
    return render(request, "carrito.html", contexto)

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect(request.META.get('HTTP_REFERER', '/'))

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('carrito')

@login_required
def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "⚠️ Tu carrito está vacío")
        return redirect('carrito')

    total = 0
    orden = Orden.objects.create(usuario=request.user, total=0)

    for producto_id_str, cantidad in carrito.items():
        producto_id = int(producto_id_str)
        producto = None
        for modelo in [Pizza, Promocion, Acompanamiento, Extra]:
            try:
                producto = modelo.objects.get(id=producto_id)
                break
            except modelo.DoesNotExist:
                continue
        if producto:
            subtotal = producto.precio * cantidad
            total += subtotal
            OrdenItem.objects.create(
                orden=orden,
                nombre=producto.nombre,
                cantidad=cantidad,
                precio=producto.precio
            )

    orden.total = total
    orden.save()
    request.session['carrito'] = {}
    messages.success(request, "✅ Tu compra fue registrada correctamente")
    return redirect('historial')

# ------------------------------
# Historial de compras
# ------------------------------
@login_required
def historial(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, "historial.html", {"ordenes": ordenes})

# ------------------------------
# LISTA DE PRODUCTOS
# ------------------------------
def pizzas(request):
    lista_pizzas = Pizza.objects.all()
    return render(request, "pizzas.html", {"pizzas": lista_pizzas})

def promociones(request):
    lista_promos = Promocion.objects.all()
    return render(request, "promociones.html", {"promociones": lista_promos})

def acompanamientos(request):
    lista_acomp = Acompanamiento.objects.all()
    return render(request, "acompanamientos.html", {"acompanamientos": lista_acomp})

def extras(request):
    lista_extras = Extra.objects.all()
    return render(request, "extras.html", {"extras": lista_extras})
