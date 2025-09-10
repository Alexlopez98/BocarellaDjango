from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    ROLES = (
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')

    def __str__(self):
        return f"{self.user.username} ({self.rol})"




class Pizza(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to="pizzas/")

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to="promociones/")

    def __str__(self):
        return self.titulo


class Acompanamiento(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to="acompanamientos/")

    def __str__(self):
        return self.nombre


class Extra(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to="extras/")

    def __str__(self):
        return self.nombre