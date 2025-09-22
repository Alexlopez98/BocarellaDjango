
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Perfil(models.Model):
    ROLES = (
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


class Pizza(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    imagen = models.ImageField(upload_to="media/")

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    imagen = models.ImageField(upload_to="promociones/")

    def __str__(self):
        return self.nombre


class Acompanamiento(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    imagen = models.ImageField(upload_to="acompanamientos/")

    def __str__(self):
        return self.nombre


class Extra(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    imagen = models.ImageField(upload_to="extras/")

    def __str__(self):
        return self.nombre


# 🔹 NUEVO: Modelos para el historial
class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    recibido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordenes_recibidas',
        limit_choices_to={'perfil__rol': 'empleado'}
    )

    # 🔹 NUEVO: Estado interno para cocina
    ESTADOS_COCINA = [
        ('pendiente', 'Pendiente'),        # Orden recibida pero no comenzada
        ('preparacion', 'En preparación'), # Cocina trabajando
        ('lista', 'Lista para salida'),    # Preparación terminada
    ]
    estado_cocina = models.CharField(
        max_length=20,
        choices=ESTADOS_COCINA,
        default='pendiente'
    )

    def __str__(self):
        return f"Orden #{self.id} de {self.usuario.username} - {self.get_estado_cocina_display()}"

    def tiempo_transcurrido_ms(self):
        """Retorna milisegundos desde la creación"""
        delta = timezone.now() - self.fecha
        return int(delta.total_seconds() * 1000)

    def tiempo_legible(self):
        """Retorna tiempo en formato 1d 2h 35m 10s"""
        delta = timezone.now() - self.fecha
        total_segundos = int(delta.total_seconds())

        dias = total_segundos // 86400
        total_segundos %= 86400

        horas = total_segundos // 3600
        total_segundos %= 3600

        minutos = total_segundos // 60
        segundos = total_segundos % 60

        partes = []
        if dias > 0:
            partes.append(f"{dias}d")
        if horas > 0:
            partes.append(f"{horas}h")
        if minutos > 0:
            partes.append(f"{minutos}m")
        if segundos > 0 or not partes:
            partes.append(f"{segundos}s")

        return " ".join(partes)



class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name="items", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)

    @property
    def subtotal(self):
        return self.cantidad * self.precio
