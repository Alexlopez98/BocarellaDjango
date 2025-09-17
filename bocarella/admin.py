from django.contrib import admin
from .models import Perfil, Pizza, Promocion, Acompanamiento, Extra

# ----------------------------
# Perfil
# ----------------------------
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion', 'rol')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)


# ----------------------------
# Pizza
# ----------------------------
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# ----------------------------
# Promoción
# ----------------------------
@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# ----------------------------
# Acompañamiento
# ----------------------------
@admin.register(Acompanamiento)
class AcompanamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# ----------------------------
# Extra
# ----------------------------
@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    ordering = ('nombre',)
