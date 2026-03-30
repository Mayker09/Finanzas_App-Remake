from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from apps.usuarios.models import Usuario
from apps.cuentas.models import Cuenta
from apps.transacciones.models import Categoria


class Presupuesto(models.Model):
    """
    Visto en: Planificación Financiera – Presupuestos Mensuales
    (Alimentación $600 – 75%, Vivienda y Renta $1,200 – 100%, Entretenimiento – excedido 120%)
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('a_tiempo', 'A tiempo'),
        ('pagado', 'Pagado'),
        ('excedido', 'Excedido'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='presupuestos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='presupuestos')
    monto_limite = models.DecimalField(
        max_digits=14, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    mes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anio = models.PositiveSmallIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        unique_together = ('usuario', 'categoria', 'mes', 'anio')
        ordering = ['-anio', '-mes']

    def __str__(self):
        return f'{self.categoria.nombre} – {self.mes}/{self.anio} (límite: ${self.monto_limite})'

    @property
    def monto_gastado(self) -> Decimal:
        """Suma real de gastos en esta categoría para el periodo."""
        # Import local para evitar importación circular
        from apps.transacciones.models import Transaccion
        resultado = Transaccion.objects.filter(
            usuario=self.usuario,
            categoria=self.categoria,
            tipo='gasto',
            fecha__month=self.mes,
            fecha__year=self.anio,
        ).aggregate(total=Sum('monto'))
        return resultado['total'] or Decimal('0.00')

    @property
    def porcentaje_usado(self) -> float:
        if not self.monto_limite:
            return 0.0
        return round(float(self.monto_gastado / self.monto_limite) * 100, 1)


class MetaAhorro(models.Model):
    """
    Visto en: Planificación Financiera – Metas de Ahorro
    (Coche Nuevo 25%, Viaje a Europa 90% ⭐, Fondo de Emergencia 80%)
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='metas_ahorro')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True)
    monto_meta = models.DecimalField(
        max_digits=14, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    monto_actual = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    fecha_objetivo = models.DateField(null=True, blank=True, help_text='Null = sin fecha límite')
    destacada = models.BooleanField(default=False, help_text='Marcada con estrella ⭐')
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Meta de Ahorro'
        verbose_name_plural = 'Metas de Ahorro'
        ordering = ['-destacada', 'fecha_objetivo']

    def __str__(self):
        return f'{self.nombre} – {self.porcentaje_completado}% completado'

    @property
    def porcentaje_completado(self) -> float:
        if not self.monto_meta:
            return 0.0
        return round(float(self.monto_actual / self.monto_meta) * 100, 1)


class PagoRecurrente(models.Model):
    """
    Visto en: Dashboard – Próximos Pagos (Alquiler $1,200 – vence en 7 días)
    """
    FRECUENCIA_CHOICES = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('anual', 'Anual'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos_recurrentes')
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='pagos_recurrentes')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='pagos_recurrentes',
    )
    nombre = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, default='mensual')
    proximo_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago Recurrente'
        verbose_name_plural = 'Pagos Recurrentes'
        ordering = ['proximo_vencimiento']

    def __str__(self):
        return f'{self.nombre} – ${self.monto} ({self.frecuencia})'

    @property
    def dias_para_vencimiento(self) -> int:
        from django.utils import timezone
        return (self.proximo_vencimiento - timezone.now().date()).days
