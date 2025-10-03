from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


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
    path('checkout/pago/', views.checkout_pago, name='checkout_pago'),
    path("historial/", views.historial, name="historial"),

    # Productos
    path("pizzas/", views.pizzas, name="pizzas"),
    path("promociones/", views.promociones, name="promociones"),
    path("acompanamientos/", views.acompanamientos, name="acompanamientos"),
    path("extras/", views.extras, name="extras"),
    
    # API ITEMS
    path("items/", views.loyverse_items, name="loyverse_items"),       # página HTML
    path("api/items/", views.loyverse_items_api, name="loyverse_items_api"),


    # API REST propias
    path("api/pizzas/", views.api_pizzas, name="api_pizzas"),
    path("api/pizzas/<int:id>/", views.api_pizza_detalle, name="api_pizza_detalle"),

    path("api/pedidos/", views.api_pedidos_usuario, name="api_pedidos_usuario"),
    path("api/pedidos/<int:id>/", views.api_pedido_detalle, name="api_pedido_detalle"),
    path("api/pedidos/todos/", views.api_pedidos_todos, name="api_pedidos_todos"),


    #API UBICACION 
    path('ubicacion/', views.ubicacion, name='ubicacion'),
]


handler403 = 'mi_app.views.error_403'

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

