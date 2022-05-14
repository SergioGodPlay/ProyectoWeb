from django.db import models
from django.contrib.auth import get_user_model
from Tienda.models import Producto
from django.db.models import F, Sum, FloatField

User = get_user_model()

# Create your models here.
class Pedido(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
    
    @property
    def total(self):
        return self.lineapedido_set.aggregate(

            total = Sum(F('precio') * F('cantidad'), output_field=FloatField())

        )["total"]

    class Meta:

        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

class lineaPedido(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido_id = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto_id.nombre}'

    class Meta:

        db_table = 'lineapedidos'
        verbose_name = 'Linea_pedido'
        verbose_name_plural = 'Lineas_pedidos'
        ordering = ['id']

