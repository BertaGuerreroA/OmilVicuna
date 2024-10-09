from django.contrib import admin
from import_export import resources
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from .models import (Sectores, Comunas, Ciudad, Nacionalidad, TipoDiscapacidad, Programas, Persona,
                     Oficio_Profesion, ExperienciaLaboral, Empresa, AlianzaColaborativa, OfertaEmpleo,
                     Derivacion, Visita,Motivo,Capacitacion)

# Resources for import/export
class SectoresResource(resources.ModelResource):
    class Meta:
        model = Sectores

class ComunasResource(resources.ModelResource):
    class Meta:
        model = Comunas

class CiudadResource(resources.ModelResource):
    class Meta:
        model = Ciudad

class NacionalidadResource(resources.ModelResource):
    class Meta:
        model = Nacionalidad

class TipoDiscapacidadResource(resources.ModelResource):
    class Meta:
        model = TipoDiscapacidad

class ProgramasResource(resources.ModelResource):
    class Meta:
        model = Programas

class PersonaResource(resources.ModelResource):
    class Meta:
        model = Persona

class OficioProfesionResource(resources.ModelResource):
    class Meta:
        model = Oficio_Profesion

class ExperienciaLaboralResource(resources.ModelResource):
    class Meta:
        model = ExperienciaLaboral

class EmpresaResource(resources.ModelResource):
    class Meta:
        model = Empresa

class AlianzaColaborativaResource(resources.ModelResource):
    class Meta:
        model = AlianzaColaborativa

class OfertaEmpleoResource(resources.ModelResource):
    class Meta:
        model = OfertaEmpleo

class DerivacionResource(resources.ModelResource):
    class Meta:
        model = Derivacion

class VisitaResource(resources.ModelResource):
    class Meta:
        model = Visita

# Admin classes
@admin.register(Sectores)
class SectoresAdmin(ImportExportModelAdmin):
    resource_class = SectoresResource
    list_display = ('nombre',)
    search_fields = ['nombre']  # Add search fields
    list_filter = ['nombre']  # Add list filter

@admin.register(Comunas)
class ComunasAdmin(ImportExportModelAdmin):
    resource_class = ComunasResource
    list_display = ('nombre',)
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(Ciudad)
class CiudadAdmin(ImportExportModelAdmin):
    resource_class = CiudadResource
    list_display = ('nombre',)
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(Nacionalidad)
class NacionalidadAdmin(ImportExportModelAdmin):
    resource_class = NacionalidadResource
    list_display = ('nombre',)
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(TipoDiscapacidad)
class TipoDiscapacidadAdmin(ImportExportModelAdmin):
    resource_class = TipoDiscapacidadResource
    list_display = ('nombre',)
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(Programas)
class ProgramasAdmin(ImportExportModelAdmin):
    resource_class = ProgramasResource
    list_display = ('nombre',)
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(Persona)
class PersonaAdmin(ImportExportModelAdmin):
    resource_class = PersonaResource
    list_display = ('rut', 'pasaporte','nombre_completo', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'nacionalidad')
    search_fields = ['rut','pasaporte', 'nombre_completo', 'apellido_paterno', 'apellido_materno']
    list_filter = ['profesion_oficio']
    autocomplete_fields = ['nacionalidad']  # Autocomplete field for foreign key
    filter_horizontal = ['profesion_oficio']  # Similar a la asignación de permisos

    # Validar si el RUT ya existe
    def save_model(self, request, obj, form, change):
        if not change:  # Solo para nuevos objetos
            if Persona.objects.filter(rut=obj.rut).exists():
                raise ValidationError(f"Una persona con el RUT {obj.rut} ya existe.")
        super().save_model(request, obj, form, change)


@admin.register(Oficio_Profesion)
class OficioProfesionAdmin(ImportExportModelAdmin):
    resource_class = OficioProfesionResource
    list_display = ('nombre',)
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(ImportExportModelAdmin):
    resource_class = ExperienciaLaboralResource
    list_display = ('empresa', 'cargo', 'fecha_inicio', 'fecha_fin')
    search_fields = ['empresa', 'cargo']
    list_filter = ['empresa', 'fecha_inicio', 'fecha_fin']


@admin.register(Empresa)
class EmpresaAdmin(ImportExportModelAdmin):
    resource_class = EmpresaResource
    list_display = ('nombre', 'rut', 'actividad_economica', 'tamagno_empresa', 'cantidad_trabajadores')
    search_fields = ['nombre', 'rut']
    list_filter = ['actividad_economica', 'tamagno_empresa', 'cantidad_trabajadores']

@admin.register(AlianzaColaborativa)
class AlianzaColaborativaAdmin(ImportExportModelAdmin):
    resource_class = AlianzaColaborativaResource
    list_display = ('nombre', 'descripcion')
    search_fields = ['nombre']
    list_filter = ['nombre']

@admin.register(OfertaEmpleo)


class OfertaEmpleoAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de objetos en el admin
    list_display = (
        'id_bne',
        'empresa',
        'fecha_creacion',
        'estado_oferta',
        'seguimiento',
        'fecha_prevista_incorporacion',
        'comuna_trabajo'
    )

    # Campos que se pueden usar para buscar
    search_fields = (
        'id_bne',
        'empresa__nombre',  # Permite buscar por el nombre de la empresa relacionada
        'nombre_solicitante',
        'run_solicitante'
    )

    # Filtros para el panel lateral
    list_filter = (
        'estado_oferta',
        'estado_seguimiento',
        'seguimiento',
        'fecha_creacion',
        'ciudad_trabajo'
    )

    # Campos que se mostrarán en el formulario de edición
    fieldsets = (
        (None, {
            'fields': (
                'id_bne',
                'empresa',
                'lugar_trabajo_obra',
                'comuna_trabajo',
                'ciudad_trabajo',
                'alianza_colaborativa'
            )
        }),
        ('Detalles del Puesto', {
            'fields': (
                'ocupacion_ofrecida',
                'experiencia_requerida',
                'escolaridad_requerida',
                'sexo_requerido',
                'rango_salarios',
                'jornada_trabajo',
                'relacion_contractual',
                'actividades_trabajador'
            )
        }),
        ('Seguimiento y Estado', {
            'fields': (
                'seguimiento',
                'estado_seguimiento',
                'estado_oferta',
                'observaciones_seguimiento',
                'fecha_prevista_incorporacion',
            )
        }),
        ('Datos del Solicitante', {
            'fields': (
                'nombre_solicitante',
                'run_solicitante',
                'fecha_nacimiento_solicitante',
                'cargo_solicitante'
            )
        }),
        ('Requisitos Adicionales', {
            'fields': (
                'licencia_conducir_requerida',
                'nacionalidad'
            )
        }),
    )

    # Orden de los registros en la lista
    ordering = ('-fecha_creacion',)

# Registrar el modelo en el admin
# admin.site.register(OfertaEmpleo, OfertaEmpleoAdmin)


@admin.register(Derivacion)
class DerivacionAdmin(ImportExportModelAdmin):
    resource_class = DerivacionResource
    list_display = ('persona', 'oferta_empleo', 'fecha_derivacion', 'estado')
    search_fields = ['persona__nombre_completo', 'oferta_empleo__titulo']  # Search by related field
    list_filter = ['estado', 'fecha_derivacion']
    autocomplete_fields = ['persona', 'oferta_empleo']  # Autocomplete for foreign keys

@admin.register(Visita)
class VisitaAdmin(ImportExportModelAdmin):
    resource_class = VisitaResource
    list_display = ('persona', 'registro_bne',  'fecha_visita')
    search_fields = ['persona__nombre_completo', 'registro_bne']
    list_filter = ['fecha_visita', 'motivo', 'registro_bne']
    autocomplete_fields = ['persona']  # Autocomplete for foreign key
    filter_horizontal = ['motivo', 'capacitaciones', 'oferta_empleo']

admin.site.register(Motivo)
admin.site.register(Capacitacion)
