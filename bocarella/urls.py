from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Carrito
    path("carrito/", views.ver_carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("checkout/", views.checkout, name="checkout"),
    path("historial/", views.historial, name="historial"),

    # Productos
    path("pizzas/", views.pizzas, name="pizzas"),
    path("promociones/", views.promociones, name="promociones"),
    path("acompanamientos/", views.acompanamientos, name="acompanamientos"),
    path("extras/", views.extras, name="extras"),
]
