from django.contrib import admin
from .models import *
from django.core.exceptions import ValidationError
from django.forms import RadioSelect

class EtapaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreetapa', 'numetapa', 'tipo_pregunta', 'id_paciente')

    # Validar que no exista una etapa con el mismo 'numetapa' para el paciente
    def save_model(self, request, obj, form, change):
        if Etapa.objects.filter(id_paciente=obj.id_paciente, numetapa=obj.numetapa).exists():
            raise ValidationError(f"Ya existe una etapa {obj.numetapa} para este paciente.")

        # Automatizar el nombre de la etapa basado en 'numetapa'
        if obj.numetapa == 1:
            obj.nombreetapa = "1: Preguntas de selección"
            obj.tipo_pregunta = "MULTIPLE"
        elif obj.numetapa == 2:
            obj.nombreetapa = "2: Examen físico"
            obj.tipo_pregunta = "EXPLORACIONES"
        elif obj.numetapa == 3:
            obj.nombreetapa = "3: Diagnóstico"
            obj.tipo_pregunta = "ESCRITA"
        
        super().save_model(request, obj, form, change)

    # Personalizamos el formulario para usar los radio buttons en numetapa
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "numetapa":
            kwargs['widget'] = RadioSelect(choices=[
                (1, '1: Preguntas de selección'),
                (2, '2: Examen físico'),
                (3, '3: Diagnóstico'),
            ])
        return super().formfield_for_dbfield(db_field, **kwargs)

    # Hacer "Nombre Etapa" no editable en el admin
    def get_readonly_fields(self, request, obj=None):
        # Aquí se asegura de que el campo 'nombreetapa' no sea editable en el admin
        return super().get_readonly_fields(request, obj) + ('nombreetapa',)

admin.site.register(TipoCaso)
admin.site.register(Paciente)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(Pregunta)
admin.site.register(OpcionMultiple)
admin.site.register(Registro)
admin.site.register(EtapaCompletada)
admin.site.register(Exploracion)