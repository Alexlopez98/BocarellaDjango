from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("acceso/", views.acceso, name="acceso"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("pizzas/", views.pizzas, name="pizzas"),
    path("promociones/", views.promociones, name="promociones"),
    path("acompanamientos/", views.acompanamientos, name="acompanamientos"),
    path("extras/", views.extras, name="extras"),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),
]
