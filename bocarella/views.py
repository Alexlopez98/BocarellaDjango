from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
import json

from .decorators import rol_requerido
from .models import Perfil, Pizza, Promocion, Acompanamiento, Extra, Orden, OrdenItem
from .forms import RegistroForm, PerfilForm

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import PizzaSerializer, OrdenSerializer

from .loyverse import LoyverseAPI # ESTO VIENE EN LA DOCUMENTACION DE LOYVERSE PUNTO DE VENTA DE DONDE SACAMOS LA API

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
            if hasattr(user, 'perfil'):
                if user.perfil.rol == 'empleado':
                    return redirect('ordenes_empleados')
                elif user.perfil.rol == 'admin':
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
            update_session_auth_hash(request, user)
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
@rol_requerido(['admin'])
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# ------------------------------
# Carrito
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
        if tipo == "pizza": producto = get_object_or_404(Pizza, id=producto_id)
        elif tipo == "promocion": producto = get_object_or_404(Promocion, id=producto_id)
        elif tipo == "acompanamiento": producto = get_object_or_404(Acompanamiento, id=producto_id)
        elif tipo == "extra": producto = get_object_or_404(Extra, id=producto_id)

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

@require_POST
@csrf_exempt
def agregar_carrito(request, tipo, id):
    carrito = request.session.get('carrito', {})
    key = f"{tipo}_{id}"
    carrito[key] = carrito.get(key, 0) + 1
    request.session['carrito'] = carrito

    producto = None
    if tipo == "pizza": producto = get_object_or_404(Pizza, id=id)
    elif tipo == "promocion": producto = get_object_or_404(Promocion, id=id)
    elif tipo == "acompanamiento": producto = get_object_or_404(Acompanamiento, id=id)
    elif tipo == "extra": producto = get_object_or_404(Extra, id=id)

    subtotal = producto.precio * carrito[key]
    return JsonResponse({"qty": carrito[key], "subtotal": subtotal, "total_items": sum(carrito.values())})

@require_POST
@csrf_exempt
def eliminar_carrito(request, tipo, id):
    carrito = request.session.get('carrito', {})
    key = f"{tipo}_{id}"

    if key in carrito:
        carrito[key] -= 1
        if carrito[key] <= 0:
            del carrito[key]
        request.session['carrito'] = carrito

        producto = None
        if tipo == "pizza": producto = get_object_or_404(Pizza, id=id)
        elif tipo == "promocion": producto = get_object_or_404(Promocion, id=id)
        elif tipo == "acompanamiento": producto = get_object_or_404(Acompanamiento, id=id)
        elif tipo == "extra": producto = get_object_or_404(Extra, id=id)

        subtotal = producto.precio * carrito.get(key, 0)
        return JsonResponse({"qty": carrito.get(key, 0), "subtotal": subtotal, "total_items": sum(carrito.values())})

    return JsonResponse({"qty": 0, "subtotal": 0, "total_items": sum(carrito.values())})

@require_POST
@csrf_exempt
def agregar_carrito_cantidad(request):
    try:
        data = json.loads(request.body)
        tipo = data.get("tipo")
        id = int(data.get("id"))
        cantidad = int(data.get("cantidad", 1))
    except (ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if cantidad <= 0:
        return JsonResponse({"error": "Cantidad debe ser mayor que cero"}, status=400)

    carrito = request.session.get("carrito", {})
    key = f"{tipo}_{id}"
    carrito[key] = carrito.get(key, 0) + cantidad
    request.session["carrito"] = carrito

    producto = None
    if tipo == "pizza": producto = get_object_or_404(Pizza, id=id)
    elif tipo == "promocion": producto = get_object_or_404(Promocion, id=id)
    elif tipo == "acompanamiento": producto = get_object_or_404(Acompanamiento, id=id)
    elif tipo == "extra": producto = get_object_or_404(Extra, id=id)

    subtotal = producto.precio * carrito[key]

    return JsonResponse({
        "qty": carrito[key],
        "subtotal": subtotal,
        "total_items": sum(carrito.values())
    })

@require_POST
def vaciar_carrito(request):
    request.session['carrito'] = {}
    messages.success(request, "✅ Carrito vaciado correctamente")
    return redirect('carrito')

# ------------------------------
# Checkout
# ------------------------------
@login_required(login_url='login')
@rol_requerido(['usuario'])
def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "⚠️ Tu carrito está vacío")
        return redirect('carrito')

    total = 0
    orden = Orden.objects.create(usuario=request.user, total=0)

    for pid, cantidad in carrito.items():
        try:
            tipo, producto_id = pid.split("_")
            producto_id = int(producto_id)
        except ValueError:
            continue

        producto = None
        if tipo == "pizza": producto = Pizza.objects.filter(id=producto_id).first()
        elif tipo == "promocion": producto = Promocion.objects.filter(id=producto_id).first()
        elif tipo == "acompanamiento": producto = Acompanamiento.objects.filter(id=producto_id).first()
        elif tipo == "extra": producto = Extra.objects.filter(id=producto_id).first()

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


@login_required(login_url='login')
@rol_requerido(['usuario'])
def checkout_pago(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "⚠️ Tu carrito está vacío")
        return redirect('carrito')

    # Calcular total
    total = 0
    for pid, cantidad in carrito.items():
        try:
            tipo, producto_id = pid.split("_")
            producto_id = int(producto_id)
        except ValueError:
            continue

        producto = None
        if tipo == "pizza": producto = Pizza.objects.filter(id=producto_id).first()
        elif tipo == "promocion": producto = Promocion.objects.filter(id=producto_id).first()
        elif tipo == "acompanamiento": producto = Acompanamiento.objects.filter(id=producto_id).first()
        elif tipo == "extra": producto = Extra.objects.filter(id=producto_id).first()

        if producto:
            total += producto.precio * cantidad

    if request.method == 'POST':
        numero_tarjeta = request.POST.get('numero_tarjeta', '')
        if not validar_tarjeta_luhn(numero_tarjeta):
            messages.error(request, "❌ Número de tarjeta inválido")
            return render(request, 'checkout_pago.html', {'total': total})

        # Crear orden
        orden = Orden.objects.create(usuario=request.user, total=0)
        total_orden = 0

        for pid, cantidad in carrito.items():
            try:
                tipo, producto_id = pid.split("_")
                producto_id = int(producto_id)
            except ValueError:
                continue

            producto = None
            if tipo == "pizza": producto = Pizza.objects.filter(id=producto_id).first()
            elif tipo == "promocion": producto = Promocion.objects.filter(id=producto_id).first()
            elif tipo == "acompanamiento": producto = Acompanamiento.objects.filter(id=producto_id).first()
            elif tipo == "extra": producto = Extra.objects.filter(id=producto_id).first()

            if producto:
                subtotal = producto.precio * cantidad
                total_orden += subtotal
                OrdenItem.objects.create(
                    orden=orden,
                    nombre=producto.nombre,
                    cantidad=cantidad,
                    precio=producto.precio
                )

        orden.total = total_orden
        orden.save()
        request.session['carrito'] = {}  # vaciar carrito

        # Renderizar pantalla de pago exitoso
        return render(request, 'pagoexitoso.html', {'orden': orden})

    return render(request, 'checkout_pago.html', {'total': total})


def validar_tarjeta_luhn(numero):
    """
    Valida un número de tarjeta usando el algoritmo de Luhn.
    Retorna True si es válido, False si no.
    """
    numero = numero.replace(" ", "")  # eliminar espacios
    if not numero.isdigit():
        return False

    total = 0
    reverse_digits = numero[::-1]

    for i, d in enumerate(reverse_digits):
        n = int(d)
        if i % 2 == 1:  # duplicar cada segundo dígito
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0



# ------------------------------
# Historial de compras
# ------------------------------
@login_required
@rol_requerido(['usuario'])
def historial(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, "historial.html", {"ordenes": ordenes})

# ------------------------------
# Productos
# ------------------------------
def pizzas(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    return render(request, "pizzas.html", {"pizzas": Pizza.objects.all()})

def promociones(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    return render(request, "promociones.html", {"promociones": Promocion.objects.all()})

def acompanamientos(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    return render(request, "acompanamientos.html", {"acompanamientos": Acompanamiento.objects.all()})

def extras(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}
    return render(request, "extras.html", {"extras": Extra.objects.all()})

# ------------------------------
# Órdenes empleados
# ------------------------------
@login_required
@rol_requerido(['empleado'])
def ordenes_empleados(request):
    ordenes = Orden.objects.all().order_by('-fecha')
    total_recibido = sum(orden.total for orden in ordenes)
    return render(request, 'ordenes.html', {'ordenes': ordenes, 'total_recibido': total_recibido})

@login_required
@rol_requerido(['empleado'])
def ordenes_empleados_json(request):
    estado_filtro = request.GET.get('estado', 'todas')  # recibe el filtro desde JS

    ordenes = Orden.objects.all().order_by('-fecha')
    if estado_filtro != 'todas':
        ordenes = ordenes.filter(estado_cocina=estado_filtro)

    data = []
    for orden in ordenes:
        items = [{"nombre": item.nombre, "cantidad": item.cantidad, "subtotal": item.subtotal} for item in orden.items.all()]
        data.append({
            "id": orden.id,
            "usuario": orden.usuario.username,
            "timestamp": orden.tiempo_transcurrido_ms(),
            "tiempo_legible": orden.tiempo_legible(),
            "total": orden.total,
            "items": items,
            "recibido_por": orden.recibido_por.username if orden.recibido_por else "Sin asignar",
            "estado_cocina": orden.estado_cocina or "pendiente",
        })

    return JsonResponse({"ordenes": data, "total_recibido": sum(orden.total for orden in ordenes)})

@login_required
@rol_requerido(['empleado'])
@require_POST
def avanzar_estado_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)

    try:
        data = json.loads(request.body)
        nuevo_estado = data.get('estado')
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)

    if nuevo_estado in ["pendiente", "preparacion", "lista"]:
        orden.estado_cocina = nuevo_estado
        orden.save()
        return JsonResponse({"ok": True, "estado": orden.estado_cocina})
    else:
        return JsonResponse({"ok": False, "error": "Estado inválido"}, status=400)

# ------------------------------
# Error handler
# ------------------------------
def error_403(request, exception=None):
    return render(request, '403.html', status=403)


from django.db.models import Sum
from django.utils.timezone import now, timedelta

@login_required
@rol_requerido(['empleado'])
def historial_empleado(request):
    periodo = request.GET.get("periodo", "hoy")  # valor por defecto: hoy
    fecha_inicio = None
    fecha_fin = now()

    if periodo == "hoy":
        fecha_inicio = fecha_fin.replace(hour=0, minute=0, second=0, microsecond=0)
    elif periodo == "semana":
        fecha_inicio = fecha_fin - timedelta(days=fecha_fin.weekday())
        fecha_inicio = fecha_inicio.replace(hour=0, minute=0, second=0, microsecond=0)
    elif periodo == "mes":
        fecha_inicio = fecha_fin.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif periodo == "año":
        fecha_inicio = fecha_fin.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif periodo == "personalizado":
        inicio_str = request.GET.get("inicio")
        fin_str = request.GET.get("fin")
        if inicio_str and fin_str:
            from datetime import datetime
            fecha_inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fin_str, "%Y-%m-%d")

    ordenes = Orden.objects.all().order_by('-fecha')
    if fecha_inicio:
        ordenes = ordenes.filter(fecha__range=(fecha_inicio, fecha_fin))

    total_ganado = ordenes.aggregate(total=Sum('total'))['total'] or 0

    return render(request, "historialempleados.html", {
        "ordenes": ordenes,
        "total_ganado": total_ganado,
        "periodo_actual": periodo
    })

def loyverse_items(request):
    return render(request, "loyverse.html")

def loyverse_items_api(request):
    api = LoyverseAPI()
    try:
        data = api.get_items()
        items = data.get("items", [])
    except Exception as e:
        return JsonResponse({"error": f"No se pudo conectar con Loyverse: {e}"})
    
    return JsonResponse({"items": items})


# -------------------
# API CRUD de Pizzas (Públicas)
# -------------------
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def api_pizzas(request):
    if request.method == 'GET':
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.AllowAny])
def api_pizza_detalle(request, id):
    try:
        pizza = Pizza.objects.get(id=id)
    except Pizza.DoesNotExist:
        return Response({"error": "Pizza no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PizzaSerializer(pizza)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PizzaSerializer(pizza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pizza.delete()
        return Response({"message": "Pizza eliminada"}, status=status.HTTP_204_NO_CONTENT)


# -------------------
# API CRUD de Pedidos (Protegidas con Token)
# -------------------
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def api_pedidos_usuario(request):
    if request.method == 'GET':
        pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha')
        serializer = OrdenSerializer(pedidos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['usuario'] = request.user.id
        serializer = OrdenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def api_pedido_detalle(request, id):
    try:
        pedido = Orden.objects.get(id=id, usuario=request.user)
    except Orden.DoesNotExist:
        return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdenSerializer(pedido)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrdenSerializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pedido.delete()
        return Response({"message": "Pedido eliminado"}, status=status.HTTP_204_NO_CONTENT)


# -------------------
# API Pedidos (solo Admin)
# -------------------
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def api_pedidos_todos(request):
    pedidos = Orden.objects.all().order_by('-fecha')
    serializer = OrdenSerializer(pedidos, many=True)
    return Response(serializer.data)

# google maps tienda
def ubicacion(request):
    """
    Renderiza la página con un mapa mostrando varias tiendas usando Leaflet + OpenStreetMap.
    """
    # Lista de tiendas con nombre y coordenadas
    tiendas = [
        {"nombre": "La Bocarella Valparaíso", "lat": -33.0472, "lng": -71.6127},
        {"nombre": "La Bocarella Viña del Mar", "lat": -33.0240, "lng": -71.5515},
    ]
    return render(request, "ubicaciontienda.html", {"tiendas": tiendas})
