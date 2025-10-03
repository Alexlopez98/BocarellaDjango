from rest_framework import serializers
from .models import Pizza, Orden, OrdenItem

# 🔹 Serializador de Pizzas
class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ["id", "nombre", "descripcion", "precio", "imagen"]


# 🔹 Serializador de Items de Orden
class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = ["id", "nombre", "cantidad", "precio", "subtotal"]


# 🔹 Serializador de Órdenes
class OrdenSerializer(serializers.ModelSerializer):
    items = OrdenItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orden
        fields = ["id", "usuario", "fecha", "total", "estado_cocina", "items"]
