from django.db import models
from django.contrib.auth import get_user_model
from Tienda.models import Producto
from django.db.models import F, Sum, FloatField

User = get_user_model()

#Clase Pedido para crear la tabla pedidos
class Pedido(models.Model):

    #Campo para almacenar el usuario activo que realiza el pedido
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 
    #Campo para almacenar la fecha y hora en la que ser realizo el pedido
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
    
    @property
    def total(self):
        return self.lineapedido_set.aggregate(

            total = Sum(F('precio') * F('cantidad'), output_field = FloatField())

        )["total"]

    #Clase meta para guardar el nombre de la tabla tanto en singular y plural
    class Meta:

        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

#Clase LineaPedido que crea la tabla lineapedidos
class LineaPedido(models.Model):
    
    #Campo para almacenar el usuario activo que realiza el pedido
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Campo para almacenar el producto que eligio el usuario (* NO HACE FALTA COLOCAR _id despues del nombre del campo
    #esto se hace de forma automatica por la base de datos)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
   
        if self.cantidad == 1:

            return f'{self.cantidad} unidad de {self.producto.nombre}'

        else:

            return f'{self.cantidad} unidades de {self.producto.nombre}'
    

    #Clase meta para guardar el nombre de la tabla tanto en singular y plural
    class Meta:

        db_table = 'lineapedidos'
        verbose_name = 'Linea pedido'
        verbose_name_plural = 'Lineas pedidos'
        ordering = ['id']

