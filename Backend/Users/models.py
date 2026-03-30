from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Usuario(AbstractUser):
    """
    Extiende el usuario base de Django.
    Visto en: sidebar (Juan Pérez – Plan Premium, Alex Morgan – Premium Account)
    """
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    puntaje_crediticio = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(300), MaxValueValidator(850)],
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name()} ({self.plan})'
