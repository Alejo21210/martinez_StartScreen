from rest_framework import serializers
from .models import Genero, Pelicula


class GeneroSerializer(serializers.ModelSerializer):
    total_peliculas = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Genero
        fields = ["id", "nombre", "total_peliculas"]

    def get_total_peliculas(self, obj):
        return obj.peliculas.filter(en_cartelera=True).count()


class PeliculaSerializer(serializers.ModelSerializer):
    genero_nombre = serializers.CharField(source="genero.nombre", read_only=True)

    class Meta:
        model = Pelicula
        fields = [
            "id",
            "titulo",
            "codigo",
            "duracion_minutos",
            "precio_entrada",
            "en_cartelera",
            "genero",
            "genero_nombre",
        ]
