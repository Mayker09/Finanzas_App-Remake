from django.db import models

# Create your models here.
class presupuesto(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10) # 'ingreso' o 'gasto'
