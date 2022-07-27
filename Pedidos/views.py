from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Carro.carro import Carro
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from Pedidos.models import Pedido, LineaPedido

#El decorador @login_required redirecciona en caso de que el usuario no este logeado
@login_required(login_url = "/autenticacion/logear")
def procesar_pedido(request):

    pedido = Pedido.objects.create(user = request.user)
    carro = Carro(request)
    lineas_pedido = list()

    #Con un bucle for recorremos elemento a elemento lo que se escogio en el carro
    for key, value in carro.carro.items():

        #El metodo append agrega los elementos del carro a la lista
        lineas_pedido.append(LineaPedido(

            producto_id = key,
            cantidad = value["cantidad"],
            user = request.user,
            pedido = pedido

        ))

    #El metodo bulk_create realiza varias intrucciones de tipo insert into de forma automatica
    #en este caso la lista con los pedidos
    LineaPedido.objects.bulk_create(lineas_pedido)

    enviar_mail(

        pedido = pedido,
        lineas_pedido = lineas_pedido,
        nombreusuario = request.user.username,
        emailusuario = request.user.email

    )

    messages.success(request, "El pedido se ha realizado correctamente, revisa tu correo")

    return redirect("../tienda")


def enviar_mail(**kwargs):

    asunto = "Gracias por realizar el pedido"
    mensaje = render_to_string("emails/pedido.html", {

        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario": kwargs.get("nombreusuario")
    })

    mensaje_texto = strip_tags(mensaje)
    from_email = "sergio_portal@hotmail.com"
    #to = kwargs.get("email_usuario")

    to = "richardgodplay@gmail.com"

    send_mail(asunto, mensaje, from_email, [to], html_message = mensaje)

