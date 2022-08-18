from django.shortcuts import render, redirect
from .forms import FormularioContacto
from django.core.mail import EmailMessage
from django.contrib import messages


def contacto(request):

    formulario_contacto = FormularioContacto()

    if request.method == "POST":

        formulario_contacto = FormularioContacto(data = request.POST)

        if formulario_contacto.is_valid():

            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            contenido = request.POST.get("contenido")

            #Barra Invertida (Alt + 92)
            email = EmailMessage("Mensaje desde App Django",

                "El usuario con nombre {} con la direccion {} escribe los siguiente:\n\n {}".format(nombre, email, contenido),

                "", ["richardgodplay@gmail.com"], reply_to = [email])

            try:
                email.send()

                messages.success(request, "Se ha enviado la informacion correctamente")

                return redirect("/contacto/?enviado")      

            except:

                #messages.warning(request, "No se ha podido enviar la informacion")

                return redirect("/contacto/?noenviado")

    return render(request, "contacto/contacto.html", {"miFormulario":formulario_contacto})
