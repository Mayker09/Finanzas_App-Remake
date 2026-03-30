from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.usuarios.models import Usuario


class ResumenMensual(models.Model):
    """
    Snapshot cacheado por mes.
    Visto en: Dashboard – Balance Total, Ahorro Mensual, barras de Flujo de Caja (ENE–JUN),
    Historial – Ingresos Totales $12,450 / Gastos Totales $8,210.32 / Balance $4,239.68
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='resumenes_mensuales')
    mes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anio = models.PositiveSmallIntegerField()
    ingresos_totales = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    gastos_totales = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    ahorro = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    balance_neto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    calculado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Resumen Mensual'
        verbose_name_plural = 'Resúmenes Mensuales'
        unique_together = ('usuario', 'mes', 'anio')
        ordering = ['-anio', '-mes']

    def __str__(self):
        return f'Resumen {self.mes}/{self.anio} – {self.usuario}'


class EvolucionPatrimonio(models.Model):
    """
    Un registro por fecha para graficar la curva de patrimonio neto.
    Visto en: Informes – Análisis de Patrimonio, gráfica de línea ($125,400 +12.4%)
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='evolucion_patrimonio')
    fecha = models.DateField()
    patrimonio_neto = models.DecimalField(max_digits=16, decimal_places=2)
    activos_totales = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal('0.00'))
    pasivos_totales = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Evolución de Patrimonio'
        verbose_name_plural = 'Evoluciones de Patrimonio'
        unique_together = ('usuario', 'fecha')
        ordering = ['fecha']

    def __str__(self):
        return f'{self.usuario} – {self.fecha}: ${self.patrimonio_neto}'


class IntensidadGasto(models.Model):
    """
    Agrupación de gastos por día de la semana y turno del día.
    Visto en: Informes – heatmap 'Intensidad de Gastos por Día'
    (Lun–Dom × Mañana / Tarde / Noche)
    """
    DIA_CHOICES = [
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'),
        (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo'),
    ]
    TURNO_CHOICES = [
        ('manana', 'Mañana'),   # 06:00–11:59
        ('tarde', 'Tarde'),     # 12:00–17:59
        ('noche', 'Noche'),     # 18:00–23:59
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intensidades_gasto')
    mes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    anio = models.PositiveSmallIntegerField()
    dia_semana = models.PositiveSmallIntegerField(choices=DIA_CHOICES)
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    total_gastado = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    num_transacciones = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Intensidad de Gasto'
        verbose_name_plural = 'Intensidades de Gasto'
        unique_together = ('usuario', 'mes', 'anio', 'dia_semana', 'turno')

    def __str__(self):
        return f'{self.get_dia_semana_display()} {self.turno} – {self.mes}/{self.anio}'
