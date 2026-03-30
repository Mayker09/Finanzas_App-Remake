from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from apps.usuarios.models import Usuario


class Cuenta(models.Model):
    """
    Visto en: columna 'Cuenta' en Historial de Transacciones
    (Visa ...4290, MasterCard ...1102, Main Savings, Brokerage A/C)
    """
    TIPO_CHOICES = [
        ('corriente', 'Corriente'),
        ('ahorro', 'Ahorro'),
        ('credito', 'Crédito'),
        ('inversion', 'Inversión'),
        ('efectivo', 'Efectivo'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cuentas')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero_ultimos_digitos = models.CharField(max_length=4, blank=True)
    saldo = models.DecimalField(
        max_digits=14, decimal_places=2,
        default=Decimal('0.00'),
    )
    moneda = models.CharField(max_length=3, default='USD')
    es_principal = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['-es_principal', 'nombre']

    def __str__(self):
        sufijo = f' ...{self.numero_ultimos_digitos}' if self.numero_ultimos_digitos else ''
        return f'{self.nombre}{sufijo} – {self.usuario}'
