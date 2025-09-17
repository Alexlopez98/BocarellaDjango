from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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

@login_required
def cambiar_clave(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # mantiene sesión activa
            messages.success(request, '✅ Contraseña actualizada correctamente')
            return redirect('perfil')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('perfil')

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

    for pid, cantidad in carrito.items():
        try:
            tipo, producto_id = pid.split("_")
            producto_id = int(producto_id)
        except:
            continue

        producto = None
        if tipo == "pizza":
            producto = get_object_or_404(Pizza, id=producto_id)
        elif tipo == "promocion":
            producto = get_object_or_404(Promocion, id=producto_id)
        elif tipo == "acompanamiento":
            producto = get_object_or_404(Acompanamiento, id=producto_id)
        elif tipo == "extra":
            producto = get_object_or_404(Extra, id=producto_id)

        if producto:
            subtotal = producto.precio * cantidad
            total += subtotal
            items.append({
                "producto": producto,
                "tipo": tipo,
                "cantidad": cantidad,
                "total": subtotal,
            })

    return render(request, "carrito.html", {"carrito": {"items": items, "total": total}})


# ----------------- AGREGAR PRODUCTO -----------------
def agregar_carrito(request, tipo, id):
    carrito = request.session.get('carrito', {})
    key = f"{tipo}_{id}"
    carrito[key] = carrito.get(key, 0) + 1
    request.session['carrito'] = carrito

    # Calcular subtotal
    producto = None
    if tipo == "pizza": producto = get_object_or_404(Pizza, id=id)
    elif tipo == "promocion": producto = get_object_or_404(Promocion, id=id)
    elif tipo == "acompanamiento": producto = get_object_or_404(Acompanamiento, id=id)
    elif tipo == "extra": producto = get_object_or_404(Extra, id=id)

    subtotal = producto.precio * carrito[key]
    return JsonResponse({"qty": carrito[key], "subtotal": subtotal})


# ----------------- ELIMINAR PRODUCTO -----------------
def eliminar_carrito(request, tipo, id):
    carrito = request.session.get('carrito', {})
    key = f"{tipo}_{id}"

    if key in carrito:
        carrito[key] -= 1
        if carrito[key] <= 0:
            del carrito[key]
        request.session['carrito'] = carrito

        # Calcular subtotal
        producto = None
        if tipo == "pizza": producto = get_object_or_404(Pizza, id=id)
        elif tipo == "promocion": producto = get_object_or_404(Promocion, id=id)
        elif tipo == "acompanamiento": producto = get_object_or_404(Acompanamiento, id=id)
        elif tipo == "extra": producto = get_object_or_404(Extra, id=id)

        subtotal = producto.precio * carrito.get(key, 0)
        return JsonResponse({"qty": carrito.get(key, 0), "subtotal": subtotal})
    else:
        return JsonResponse({"qty": 0, "subtotal": 0})



@login_required
def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "⚠️ Tu carrito está vacío")
        return redirect('carrito')

    total = 0
    orden = Orden.objects.create(usuario=request.user, total=0)

    for pid, cantidad in carrito.items():
        # Separar tipo y id
        try:
            tipo, producto_id = pid.split("_")
            producto_id = int(producto_id)
        except ValueError:
            continue  # Si el formato es incorrecto, saltamos

        producto = None
        if tipo == "pizza":
            producto = Pizza.objects.filter(id=producto_id).first()
        elif tipo == "promocion":
            producto = Promocion.objects.filter(id=producto_id).first()
        elif tipo == "acompanamiento":
            producto = Acompanamiento.objects.filter(id=producto_id).first()
        elif tipo == "extra":
            producto = Extra.objects.filter(id=producto_id).first()

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
    request.session['carrito'] = {}  # Vaciar carrito
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
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    lista_pizzas = Pizza.objects.all()
    return render(request, "pizzas.html", {"pizzas": lista_pizzas})


def promociones(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    lista_promos = Promocion.objects.all()
    return render(request, "promociones.html", {"promociones": lista_promos})


def acompanamientos(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    lista_acomp = Acompanamiento.objects.all()
    return render(request, "acompanamientos.html", {"acompanamientos": lista_acomp})


def extras(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    lista_extras = Extra.objects.all()
    return render(request, "extras.html", {"extras": lista_extras})