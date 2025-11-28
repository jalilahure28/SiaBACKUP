from django.urls import path
from . import views

app_name = 'cursosestudiante'

urlpatterns = [
    path('menu-estudiante/', views.menu_estudiante, name='menu_estudiante'),
    path('mis-cursos/', views.ListaCursosEstudianteView.as_view(), name='lista_cursos'),
    path('avances/', views.RevisarAvancesView, name='ver_avances'),
    path('editar-perfil/', views.EditarPerfilView, name='editar_perfil'),
    path('avances/', views.RevisarAvancesView, name='ver_avances'),
]