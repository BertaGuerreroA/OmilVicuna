from enum import unique
# from Scripts.pywin32_postinstall import verbose
from django.db import models
from datetime import date

class Sectores(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Sector de Residencia")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Sectores"


class Comunas(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Comuna")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Comunas"


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Ciudad")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Ciudad"


class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nacionalidad")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Nacionalidad"


class TipoDiscapacidad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Tipo de Discapacidad")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipo Discapacidad"


class Programas(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Programa")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Programas"


class Persona(models.Model):
    SITUACION_MIGRANTE_CHOICES = [
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('no_aplica', 'No Aplica'),
    ]

    ESCOLARIDAD_CHOICES = [
        ('basica_incompleta', 'Básica Incompleta'),
        ('basica_completa', 'Básica Completa'),
        ('media_incompleta', 'Media Incompleta'),
        ('media_completa', 'Media Completa'),
        ('tecnica_incompleta', 'Técnica Incompleta'),
        ('tecnica_completa', 'Técnica Completa'),
        ('universitaria_incompleta', 'Universitaria Incompleta'),
        ('universitaria_completa', 'Universitaria Completa'),
        ('postgrado', 'Postgrado'),
        ('ninguna', 'Ninguna'),
    ]

    DISCAPACIDAD_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    TIPO_DOCUMENTO_CHOICES = [
        ('RUN', 'RUN'),
        ('Pasaporte', 'Pasaporte'),
        ('Otro', 'Otro'),
    ]

    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    fecha_atencion = models.DateField(verbose_name="Fecha de Atención")
    tipo_documento = models.CharField(verbose_name="Tipo de Documento", max_length=20, choices=TIPO_DOCUMENTO_CHOICES, default='RUN')
    rut = models.CharField(max_length=12, verbose_name="RUT", unique = True)
    pasaporte = models.CharField(max_length=20, verbose_name="Pasaporte o DNI",null= True,blank=True)
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    telefono2 = models.CharField(max_length=15, verbose_name="Teléfono Secundario")
    correo_electronico = models.EmailField(verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    sector_residencia = models.ForeignKey(Sectores, on_delete=models.SET_NULL, null=True, verbose_name="Sector de Residencia")
    comuna = models.ForeignKey(Comunas, on_delete=models.SET_NULL, null=True, verbose_name="Comuna")
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, verbose_name="Ciudad")
    # Cambiar el campo a ManyToManyField para permitir múltiples oficios
    profesion_oficio = models.ManyToManyField('Oficio_Profesion', verbose_name="Profesión u Oficio",
                                              related_name='personas')
    sexo = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name="Sexo")
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.SET_NULL, null=True, verbose_name="Nacionalidad")
    derivados_programas = models.ManyToManyField(Programas, blank=True, verbose_name="Derivados de Programas")
    persona_con_discapacidad = models.CharField(max_length=2, choices=DISCAPACIDAD_CHOICES, verbose_name="Persona con Discapacidad")
    tipo_discapacidad = models.ForeignKey(TipoDiscapacidad, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Discapacidad")
    situacion_migrante = models.CharField(max_length=10, choices=SITUACION_MIGRANTE_CHOICES, verbose_name="Situación Migrante")
    escolaridad = models.CharField(max_length=30, choices=ESCOLARIDAD_CHOICES, verbose_name="Escolaridad")

    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def save(self, *args, **kwargs):
        # Convertir a "nombre propio"
        self.nombre_completo = self.nombre_completo.title()
        self.apellido_paterno = self.apellido_paterno.title()
        self.apellido_materno = self.apellido_materno.title()
        self.direccion = self.direccion.title()

        # Normalizar el correo electrónico a minúsculas
        self.correo_electronico = self.correo_electronico.lower()

        # Procesar y limpiar el RUT
        rut_sin_puntos = self.rut.replace(".", "").replace(",", "")  # Quitar puntos y comas
        cuerpo_rut = rut_sin_puntos[:-2]  # Los números antes del guion
        digito_verificador = rut_sin_puntos[-1].upper()  # El último carácter (DV), convertido a mayúscula
        self.rut = f"{cuerpo_rut}-{digito_verificador}"  # Formatear el RUT con guion

        super(Persona, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.rut) + ": " + str(self.nombre_completo) + " " + str(self.apellido_paterno)

    class Meta:
        verbose_name_plural = "Personas"


# Modelo Oficio_Profesion (anteriormente Habilidad)
class Oficio_Profesion(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Oficio Profesión"


# Modelo ExperienciaLaboral
class ExperienciaLaboral(models.Model):
    empresa = models.CharField(max_length=255, verbose_name="Empresa")
    cargo = models.CharField(max_length=255, verbose_name="Cargo")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")

    def __str__(self):
        return f'{self.cargo} en {self.empresa}'

    class Meta:
        verbose_name_plural = "Experiencia Laboral"



# Modelo Empresa
class Empresa(models.Model):
    TAMANO_EMPRESA_CHOICES = [
        ('MCR', 'Micro'),
        ('PE', 'Pequeña'),
        ('ME', 'Mediana'),
        ('GR', 'Grande'),
    ]

    TIPO_EMPRESA_CHOICES = [
        ('SPA', 'Sociedad por Acciones (SpA)'),
        ('SRL', 'Sociedad de Responsabilidad Limitada (SRL)'),
        ('SA', 'Sociedad Anónima (SA)'),
        ('EIRL', 'Empresa Individual de Responsabilidad Limitada (EIRL)'),
        ('COOP', 'Cooperativa'),
        ('FI', 'Fundación o Institución'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Empresa")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    actividad_economica = models.CharField(max_length=255, verbose_name="Actividad Económica")
    cantidad_trabajadores = models.IntegerField(verbose_name="Cantidad de Trabajadores")
    tamagno_empresa = models.CharField(max_length=3, choices=TAMANO_EMPRESA_CHOICES, blank=True, null=True, verbose_name="Tamaño de Empresa")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    contacto = models.CharField(max_length=100, verbose_name="Contacto")
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, verbose_name="Ciudad")
    comuna = models.ForeignKey(Comunas, on_delete=models.CASCADE, verbose_name="Comuna")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción de la Empresa")

    def __str__(self):
        return f'{self.rut} - {self.nombre}'

    class Meta:
        verbose_name_plural = "Empresas"


    def save(self, *args, **kwargs):

        # Procesar y limpiar el RUT
        rut_sin_puntos = self.rut.replace(".", "").replace(",", "").replace("-", "")  # Quitar puntos y comas
        cuerpo_rut = rut_sin_puntos[:-2]  # Los números antes del guion
        digito_verificador = rut_sin_puntos[-1].upper()  # El último carácter (DV), convertido a mayúscula
        self.rut = f"{cuerpo_rut}-{digito_verificador}"  # Formatear el RUT con guion

        super(Empresa, self).save(*args, **kwargs)


class AlianzaColaborativa(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Alianzas Colaborativas"


# Modelo OfertaEmpleo
class OfertaEmpleo(models.Model):
    SEGUIMIENTO_CHOICES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]

    ESTADO_SEGUIMIENTO_CHOICES = [
        ('Anulada', 'Anulada'),
        ('Cerrada con colocados', 'Cerrada con colocados'),
        ('En espera FeedBack', 'En espera FeedBack'),
        ('En proceso de selección', 'En proceso de selección'),
        ('Pausada', 'Pausada'),
        ('Vigente', 'Vigente'),
    ]

    ESTADO_OFERTA_CHOICES = [
        ('Cerrada', 'Cerrada'),
        ('Activa', 'Activa'),
    ]

    ESCOLARIDAD_CHOICES = [
        ('basica_incompleta', 'Básica Incompleta'),
        ('basica_completa', 'Básica Completa'),
        ('media_incompleta', 'Media Incompleta'),
        ('media_completa', 'Media Completa'),
        ('tecnica_incompleta', 'Técnica Incompleta'),
        ('tecnica_completa', 'Técnica Completa'),
        ('universitaria_incompleta', 'Universitaria Incompleta'),
        ('universitaria_completa', 'Universitaria Completa'),
        ('postgrado', 'Postgrado'),
        ('ninguna', 'Ninguna'),
    ]

    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    LICENCIA_CHOICES = [
        ('A1', 'Clase A1'),
        ('A2', 'Clase A2'),
        ('A3', 'Clase A3'),
        ('A4', 'Clase A4'),
        ('A5', 'Clase A5'),
        ('B', 'Clase B'),
        ('C', 'Clase C'),
        ('D', 'Clase D'),
        ('E', 'Clase E'),
        ('F', 'Clase F'),
        ('No Requiere', 'No Requiere'),
    ]

    JORNADA_TRABAJO_CHOICES = [
        ('Completa', 'Jornada Completa'),
        ('Parcial', 'Jornada Parcial/Part Time'),
        ('SinLimitacion', 'Sin limitación horaria'),
    ]

    RELACION_CONTRACTUAL_CHOICES = [
        ('obra_o_faena', 'Contrato por obra o faena'),
        ('plazo_fijo', 'Contrato a plazo fijo'),
        ('indefinido', 'Contrato indefinido'),
        ('administracion_publica', 'Administración Pública'),
        ('honorarios', 'Honorarios'),
        ('indiferente', 'Indiferente'),
    ]

    id_bne = models.CharField(max_length=255, blank=True, null=True)
    id_interno = models.CharField(max_length=50, blank=True, null=True)  # No obligatorio
    mes = models.CharField(max_length=2)  # Mes de la oferta
    fecha_creacion = models.DateField(auto_now_add=True)  # Fecha de creación de la oferta
    seguimiento = models.CharField(max_length=2, choices=SEGUIMIENTO_CHOICES, default='No')  # Seguimiento Si o No
    estado_seguimiento = models.CharField(max_length=50, choices=ESTADO_SEGUIMIENTO_CHOICES)  # Estado de seguimiento
    estado_oferta = models.CharField(max_length=10, choices=ESTADO_OFERTA_CHOICES)  # Estado de la oferta
    observaciones_seguimiento = models.TextField(blank=True, null=True)  # Observaciones de seguimiento
    fecha_prevista_incorporacion = models.DateField()  # Fecha prevista de incorporación
    ocupacion_ofrecida = models.CharField(max_length=255)  # Ocupación ofrecida
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Empresa o empleador (FK)
    nombre_solicitante = models.CharField(max_length=255)  # Nombre del solicitante
    run_solicitante = models.CharField(max_length=12)  # RUN del solicitante, sin puntos y con guion
    fecha_nacimiento_solicitante = models.DateField()  # Fecha de nacimiento del solicitante
    cargo_solicitante = models.CharField(max_length=255)  # Cargo del solicitante
    direccion_empresa = models.CharField(max_length=255)  # Dirección de la empresa
    comuna_trabajo = models.ForeignKey(Comunas, on_delete=models.CASCADE, related_name='comuna_trabajo')  # Comuna donde trabajará
    experiencia_requerida = models.PositiveIntegerField(verbose_name="Experiencia requerida (años)")  # Años de experiencia requerida
    escolaridad_requerida = models.CharField(max_length=30, choices=ESCOLARIDAD_CHOICES, verbose_name="Escolaridad")
    rango_salarios = models.CharField(max_length=50)  # Rango de salarios
    sexo_requerido = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name="Sexo")
    relacion_contractual = models.CharField(max_length=30, choices=RELACION_CONTRACTUAL_CHOICES, verbose_name="Relación Contractual")
    actividades_trabajador = models.TextField()  # Actividades del trabajador y conocimientos específicos asociados
    jornada_trabajo = models.CharField(max_length=20, choices=JORNADA_TRABAJO_CHOICES, verbose_name="Jornada de Trabajo")  # Jornada de trabajo
    licencia_conducir_requerida = models.CharField(max_length=20, choices=LICENCIA_CHOICES, blank=True, null=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.SET_NULL, null=True, verbose_name="Nacionalidad")
    lugar_trabajo_obra = models.CharField(max_length=255)  # Lugar de trabajo/obra
    ciudad_trabajo = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='ciudad_trabajo')  # Ciudad del trabajo
    alianza_colaborativa = models.ForeignKey(AlianzaColaborativa, on_delete=models.SET_NULL, null=True)  # Alianza colaborativa

    def __str__(self):
        return f'{self.ocupacion_ofrecida} - {self.empresa.nombre}'



    def save(self, *args, **kwargs):
        # Convertir a "nombre propio" (Title Case) los campos relevantes
        self.ocupacion_ofrecida = self.ocupacion_ofrecida.title()
        self.ocupacion_ofrecida = self.ocupacion_ofrecida.title()
        self.nombre_solicitante = self.nombre_solicitante.title()
        self.cargo_solicitante = self.cargo_solicitante.title()
        self.lugar_trabajo_obra = self.lugar_trabajo_obra.title()

        # Normalizar el correo electrónico a minúsculas
        # self.email_empresa = self.email_empresa.lower()

        # Procesar y limpiar el RUT del solicitante
        rut_sin_puntos_2 = self.run_solicitante.replace(".", "").replace(",", "")  # Quitar puntos y comas
        cuerpo_rut_2 = rut_sin_puntos_2[:-2]  # Los números antes del guion
        digito_verificador_2 = rut_sin_puntos_2[-1].upper()  # El último carácter (DV), convertido a mayúscula
        self.run_solicitante = f"{cuerpo_rut_2}-{digito_verificador_2}"  # Formatear el RUT con guion

        super(OfertaEmpleo, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Ofertas de Empleo"




# Modelo Derivacion
class Derivacion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='derivaciones')
    oferta_empleo = models.ForeignKey(OfertaEmpleo, on_delete=models.CASCADE, related_name='derivaciones')
    fecha_derivacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')])

    def __str__(self):
        return f'Derivación de {self.persona.nombre_completo} a {self.oferta_empleo.ocupacion_ofrecida}'
    class Meta:
        verbose_name_plural = "Derivaciones a ofertas"

class Motivo(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Motivo")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Motivos"

class Capacitacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre de la Capacitación")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción de la Capacitación")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Capacitaciones"

# Modelo Visita
class Visita(models.Model):
    REGISTRO_BNE_CHOICES = [
        ('registrado', 'Registrado'),
        ('pendiente', 'Pendiente'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='visitas')
    fecha_visita = models.DateTimeField(auto_now_add=True)
    registro_bne = models.CharField(max_length=10, choices=REGISTRO_BNE_CHOICES, default='pendiente')
    oferta_empleo = models.ManyToManyField(OfertaEmpleo, verbose_name="Oferta de Empleo", null=True, blank=True)  # Nueva relación
    motivo = models.ManyToManyField(Motivo, verbose_name="Motivos")  # Relación muchos a muchos con Motivos
    capacitaciones = models.ManyToManyField(Capacitacion, blank=True,
                                            verbose_name="Capacitaciones")  # Nueva relación con Capacitaciones
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Visita de {self.persona.nombre_completo} el {self.fecha_visita}'

    class Meta:
        verbose_name_plural = "Visitas OMIL"


