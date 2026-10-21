from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    precio_unitario = models.IntegerField()
    stock_disponible = models.IntegerField()
    requiere_refrigeracion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

class Pedido(models.Model):
    MODALIDAD_CHOICES = [
        ('PICKUP', 'Retiro en Tienda'),
        ('EXPRESS', 'Despacho Express'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=150)
    correo_cliente = models.EmailField()
    modalidad = models.CharField(max_length=10, choices=MODALIDAD_CHOICES)
    fecha_entrega = models.DateField()
    direccion = models.CharField(max_length=255)
    total_estimado = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"
