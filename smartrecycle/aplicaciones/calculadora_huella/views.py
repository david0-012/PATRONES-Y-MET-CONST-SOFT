from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pregunta, Opcion, Respuesta, Intento
from django.contrib import messages
@login_required
def cuestionario(request, pregunta_id=None):
    if request.method == 'POST':  # Si la solicitud es POST
        opcion_id = request.POST['opcion']
        opcion = Opcion.objects.get(id=opcion_id)
        ultimo_intento = Intento.objects.filter(usuario=request.user).order_by('-id').first()
        respuesta = Respuesta(usuario=request.user, intento=ultimo_intento, pregunta=opcion.pregunta, opcion=opcion)
        respuesta.save()

        # Actualizar el puntaje del intento
        ultimo_intento.puntaje += opcion.valor
        ultimo_intento.save()

        siguiente_pregunta = Pregunta.objects.filter(orden__gt=opcion.pregunta.orden).order_by('orden').first()
        if siguiente_pregunta is None:
            return redirect('resultados')
        else:
            return redirect(f'/cuestionario/{siguiente_pregunta.id}/')
    else:  # Si la solicitud es GET
        if pregunta_id is None:
            nuevo_intento = Intento(usuario=request.user)
            nuevo_intento.save()
            pregunta = Pregunta.objects.order_by('orden').first()
        else:
            nuevo_intento = Intento.objects.filter(usuario=request.user).order_by('-id').first()
            pregunta = Pregunta.objects.get(id=pregunta_id)

        return render(request, 'cuestionario.html', {'pregunta': pregunta, 'intento': nuevo_intento})

def calcular_resultados(respuestas):
    return sum(respuesta.opcion.valor for respuesta in respuestas)

@login_required
def cuestionario(request, pregunta_id=None):
    if request.method == 'POST':  # Si la solicitud es POST
        opcion_id = request.POST['opcion']
        opcion = Opcion.objects.get(id=opcion_id)
        # Obtenemos el último intento
        ultimo_intento = Intento.objects.filter(usuario=request.user).order_by('-id').first()
        # Creamos una nueva respuesta asociada con el intento actual
        respuesta = Respuesta(usuario=request.user, intento=ultimo_intento, pregunta=opcion.pregunta, opcion=opcion)
        respuesta.save()

        # Obtenemos la siguiente pregunta
        siguiente_pregunta = Pregunta.objects.filter(orden__gt=opcion.pregunta.orden).order_by('orden').first()
        if siguiente_pregunta is None:
            # Si no hay más preguntas, redirigimos al usuario a la página de resultados
            return redirect('resultados')
        else:
            # Si hay una siguiente pregunta, redirigimos al usuario a esa pregunta
            return redirect(f'/cuestionario/{siguiente_pregunta.id}/')

    else:  # Si la solicitud es GET
        if pregunta_id is None:
            # Si el usuario está comenzando el cuestionario, creamos un nuevo intento
            nuevo_intento = Intento(usuario=request.user)
            nuevo_intento.save()
        else:
            # Si el usuario está respondiendo a una pregunta, obtenemos el último intento
            nuevo_intento = Intento.objects.filter(usuario=request.user).order_by('-id').first()

        if pregunta_id is not None:
            pregunta = Pregunta.objects.get(id=pregunta_id)
        else:
            pregunta = Pregunta.objects.order_by('orden').first()

        return render(request, 'cuestionario.html', {'pregunta': pregunta, 'intento': nuevo_intento})


@login_required
def resultados(request):
    # Obtenemos todos los intentos del usuario y los ordenamos de más reciente a más antiguo
    intentos = Intento.objects.filter(usuario=request.user).order_by('-fecha')
    print(f'Intentos: {intentos}')  # Imprime los intentos

    if not intentos:
        # Si el usuario no ha hecho ningún intento, lo redirigimos a la página de inicio
        return redirect('inicio')

    # Obtenemos el último intento del usuario
    ultimo_intento = intentos[0]

    # Obtenemos todas las respuestas para el último intento
    respuestas = Respuesta.objects.filter(intento=ultimo_intento)

    # Calculamos el total y los consejos
    total = sum(respuesta.opcion.valor for respuesta in respuestas)
    consejos = [respuesta.opcion.consejo for respuesta in respuestas if respuesta.opcion.consejo]

    # Define 'total_anterior' antes del bloque 'if'
    total_anterior = 0  # o cualquier valor por defecto

    if len(intentos) > 1:
        # Obtenemos el intento anterior
        intento_anterior = intentos[1]
        respuestas_anteriores = Respuesta.objects.filter(intento=intento_anterior)
        total_anterior = sum(respuesta.opcion.valor for respuesta in respuestas_anteriores)
        if total > total_anterior:
            mejora = f"Has empeorado, tu huella aumentó a comparación de tu anterior intento {total_anterior}"
        elif total < total_anterior:
            mejora = f"Has mejorado, tu huella disminuyo a comparación de tu anterior intento {total_anterior}"
        else:
            mejora = "Tu puntaje es el mismo que el anterior"
    else:
        mejora = "Este es tu primer intento"

    # Calculamos el número de intento
    numero_de_intento = intentos.count()
    print(f'Número de intento: {numero_de_intento}')  # Imprime el número de intento

    return render(request, 'resultados.html', {'total': total, 'consejos': consejos, 'mejora': mejora, 'ultimo_intento': ultimo_intento, 'total_anterior': total_anterior, 'numero_de_intento': numero_de_intento})
@login_required
def historial(request):
    intentos = Intento.objects.filter(usuario=request.user)
    puntajes = [intento.puntaje for intento in intentos]
    return render(request, 'historial.html', {'puntajes': puntajes})
@login_required
def borrar_intentos(request):
    # Asegúrate de que el usuario esté autenticado antes de borrar sus intentos
    if request.user.is_authenticated:
        # Obtén los intentos del usuario
        intentos = Intento.objects.filter(usuario=request.user)

        # Borra los intentos del usuario
        intentos.delete()

        # Informa al usuario que sus intentos fueron borrados
        messages.success(request, 'Tus intentos han sido borrados.', extra_tags='borrar_intentos')
    else:
        # Informa al usuario que necesita autenticarse
        messages.error(request, 'Necesitas autenticarte para borrar tus intentos.')

    # Redirige al usuario a la página de inicio
    return redirect('inicio')