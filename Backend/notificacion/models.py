from django.db import models

from apps.usuarios.models import Usuario


class Notificacion(models.Model):
    """
    Visto en: ícono de campana (🔔) en el header de todas las pantallas.
    """
    TIPO_CHOICES = [
        ('alerta_presupuesto', 'Alerta de Presupuesto'),
        ('pago_proximo', 'Pago Próximo'),
        ('meta_alcanzada', 'Meta Alcanzada'),
        ('transaccion', 'Nueva Transacción'),
        ('informe', 'Informe Disponible'),
        ('general', 'General'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='general')
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-creada_en']

    def __str__(self):
        estado = 'leída' if self.leida else 'sin leer'
        return f'[{self.tipo}] {self.titulo} – {estado}'
