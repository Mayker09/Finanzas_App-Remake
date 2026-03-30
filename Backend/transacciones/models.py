from django.db import models

# Create your models here.
from decimal import Decimal

from django.db import models

from apps.usuarios.models import Usuario
from apps.cuentas.models import Cuenta


class Categoria(models.Model):
    """
    Visto en: Gastos por Categoría (Vivienda 45%, Alimentación 30%, Transporte 15%),
    tags de transacciones (Alimentación, Salario, Compras, Transporte, Inversiones).
    usuario=None significa categoría del sistema compartida para todos.
    """
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('transferencia', 'Transferencia'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    icono = models.CharField(max_length=50, blank=True, help_text='Nombre del ícono (ej: shopping-cart)')
    color = models.CharField(max_length=7, default='#007A7A', help_text='Color hex')
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='categorias',
        help_text='Null = categoría del sistema global',
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        unique_together = ('nombre', 'usuario')

    def __str__(self):
        return f'{self.nombre} ({self.tipo})'


class Transaccion(models.Model):
    """
    Visto en: Historial de Transacciones y Últimos Movimientos del Dashboard
    (Restaurante El Olivo, Nómina Mensual, Amazon.es, Uber Trip,
    Inversión Dividendos, Supermercado Central)
    """
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('transferencia', 'Transferencia'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacciones')
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='transacciones')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='transacciones',
    )

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=255)
    detalle = models.CharField(
        max_length=255, blank=True,
        help_text='Ej: Cena de negocios, Tech Solutions Corp',
    )
    monto = models.DecimalField(
        max_digits=14, decimal_places=2,
        help_text='Siempre positivo; el signo se deriva del campo tipo',
    )
    fecha = models.DateTimeField()
    notas = models.TextField(blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha']

    def __str__(self):
        signo = '+' if self.tipo == 'ingreso' else '-'
        return f'{self.descripcion} {signo}${self.monto} ({self.fecha.date()})'

    @property
    def monto_firmado(self) -> Decimal:
        """Devuelve el monto con signo negativo si es gasto."""
        if self.tipo == 'gasto':
            return -abs(self.monto)
        return abs(self.monto)
