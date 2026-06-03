from django.db import models


class Genero(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    duracion_minutos = models.PositiveIntegerField()
    precio_entrada = models.DecimalField(max_digits=10, decimal_places=2)
    en_cartelera = models.BooleanField(default=True)
    genero = models.ForeignKey(
        Genero,
        on_delete=models.PROTECT,
        related_name="peliculas",
    )

    def __str__(self):
        return f"{self.titulo} ({self.codigo})"
