from django.db import models



# Create your models here.
class tipo(models.TextChoices):
    INGRESO = 'ingreso', 'Ingreso'
    GASTO = 'gasto', 'Gasto'

class presupuesto(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10,choices=tipo.choices) # 'ingreso' o 'gasto'
