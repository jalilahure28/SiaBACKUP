from django.shortcuts import render, redirect
import json
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from applications.cursosdocente.models import Curso
from applications.login.models import Docente, Estudiante
from applications.casospacientes.models import Paciente, Etapa, EtapaCompletada
from applications.cursosestudiante.models import Avance, Enrolamiento

class ListaCursosEstudianteView(ListView):
    model = Curso
    template_name = 'cursosestudiante/listadocursos.html'
    context_object_name = 'object_list'
    
def menu_estudiante(request):
    # Verifica si el usuario tiene una sesión activa
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del estudiante de la sesión

    if not usuario_id:  # Si no hay usuario_id en la sesión, redirige al login
        return redirect('login:login_estudiante')  # Redirige al login si no está autenticado

    try:
        # Intenta obtener el estudiante con el ID almacenado en la sesión
        usuario = Estudiante.objects.get(id=usuario_id)
    except Estudiante.DoesNotExist:
        # Si el estudiante no existe, redirige al login
        return redirect('login:login_estudiante')

    # Si el estudiante existe, pasa el objeto a la plantilla
    return render(request, 'cursosestudiante/menuestudiante.html', {'user': usuario})

def RevisarAvancesView(request):
    # Obtener el estudiante logueado
    usuario_id = request.session.get('usuario_id')  # Obtener ID del estudiante desde la sesión
    if not usuario_id:
        return redirect('login:login')  # Si no hay usuario logueado, redirigir al login

    # Obtener el estudiante con el ID guardado en la sesión
    try:
        usuario = Estudiante.objects.get(id=usuario_id)
    except Estudiante.DoesNotExist:
        return redirect('login:login_estudiante')  # Redirigir si el estudiante no se encuentra

    # Obtener los cursos en los que el estudiante está inscrito
    enrolamientos = Enrolamiento.objects.filter(estudiante=usuario)
    cursos_inscritos = [enrolamiento.curso for enrolamiento in enrolamientos]

    # Obtener el avance general
    avances = Avance.objects.filter(id_estudiante=usuario)
    total_cursos = len(cursos_inscritos)
    cursos_completados = avances.filter(completado=True).count()
    porcentaje_general = (cursos_completados / total_cursos) * 100 if total_cursos > 0 else 0

    # Información de los cursos y su progreso
    cursos_info = []
    for curso in cursos_inscritos:
        # Obtener el avance del curso
        avance_curso = avances.filter(id_curso=curso).first()  # Tomamos el primer avance del curso

        # Obtener los pacientes relacionados con el curso
        pacientes = Paciente.objects.filter(id_curso=curso)

        # Obtener el progreso de cada paciente y sus etapas
        pacientes_info = []
        for paciente in pacientes:
            etapas = Etapa.objects.filter(id_paciente=paciente)
            etapas_info = []
            for etapa in etapas:
                # Verificar si la etapa ha sido completada por el estudiante
                etapa_completada = EtapaCompletada.objects.filter(estudiante=usuario, etapa=etapa).exists()
                etapas_info.append({
                    'etapa': etapa.nombreetapa,
                    'completada': etapa_completada
                })

            pacientes_info.append({
                'paciente': paciente.nombre,
                'etapas': etapas_info
            })

        cursos_info.append({
            'curso': curso.nombrecurso,
            'avance': avance_curso.porcentajeavance if avance_curso else 0,
            'pacientes': pacientes_info
        })

    return render(request, 'cursosestudiante/avances.html', {
        'cursos_info': cursos_info,
        'porcentaje_general': porcentaje_general,
        'usuario': usuario
    })

# Vista provisional para "editar perfil"
def EditarPerfilView(request):
    return HttpResponse("Esta es una vista provisional para editar el perfil.")