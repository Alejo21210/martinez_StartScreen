from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Genero, Pelicula
from .serializers import GeneroSerializer, PeliculaSerializer
from .permissions import IsAdminOrReadOnly


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all().order_by("id")
    serializer_class = GeneroSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["id", "nombre"]


class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.select_related("genero").all().order_by("id")
    serializer_class = PeliculaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["genero", "en_cartelera"]
    search_fields = ["titulo", "codigo"]
    ordering_fields = ["duracion_minutos", "id", "titulo", "precio_entrada"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return super().get_permissions()
