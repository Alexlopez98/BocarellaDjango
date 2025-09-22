from django.urls import path
from . import views

urlpatterns = [
    # Home y autenticación
    path("", views.home, name="index"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
    path('perfil/cambiar_clave/', views.cambiar_clave, name='cambiar_clave'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Órdenes empleados
    path('ordenes/', views.ordenes_empleados, name='ordenes_empleados'),
    path('ordenes/json/', views.ordenes_empleados_json, name='ordenes_empleados_json'),
    path('actualizar_estado_cocina/<int:orden_id>/', views.avanzar_estado_orden, name='actualizar_estado_cocina'),

    # Carrito
    path("carrito/", views.ver_carrito, name="carrito"),
    path("carrito/agregar/<str:tipo>/<int:id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/eliminar/<str:tipo>/<int:id>/", views.eliminar_carrito, name="eliminar_carrito"),
    path("carrito/agregar-cantidad/", views.agregar_carrito_cantidad, name="agregar_carrito_cantidad"),
    path("vaciar-carrito/", views.vaciar_carrito, name="vaciar_carrito"),

    # Checkout e historial
    path("checkout/", views.checkout, name="checkout"),
    path("historial/", views.historial, name="historial"),

    # Productos
    path("pizzas/", views.pizzas, name="pizzas"),
    path("promociones/", views.promociones, name="promociones"),
    path("acompanamientos/", views.acompanamientos, name="acompanamientos"),
    path("extras/", views.extras, name="extras"),
]

handler403 = 'mi_app.views.error_403'
