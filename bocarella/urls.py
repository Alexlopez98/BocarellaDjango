from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("acceso/", views.acceso, name="acceso"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
]
