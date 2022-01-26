from django.urls import path

from . import views

#Utilizamos un namespace con el nombre "carro" delante de la url "agregar" ,"eliminar", etc
#para evitar conflictos si tenemos url con el mismo nombre
app_name = "carro"

urlpatterns = [
    path('agregar/<int:producto_id>/',views.agregarProducto, name="agregar"),
    path('eliminar/<int:producto_id>/',views.eliminarProducto, name="eliminar"),
    path('restar/<int:producto_id>/',views.restarProducto, name="restar"),
    path('limpiar/',views.limpiarCarro, name="limpiar"),
]