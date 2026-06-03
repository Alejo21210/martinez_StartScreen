from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Genero, Pelicula
from .serializers import GeneroSerializer, PeliculaSerializer
from .permissions import IsAdminOrReadOnly


DESCUENTOS = {
    "GENERAL": 0,
    "ESTUDIANTE": 20,
    "TERCERA_EDAD": 30,
}


@api_view(["POST"])
@permission_classes([AllowAny])
def calcular_entradas(request):
    entradas = request.data.get("entradas", [])
    if not isinstance(entradas, list):
        return Response(
            {"error": "Se requiere un arreglo 'entradas'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    detalle = []
    total = 0

    for item in entradas:
        try:
            precio_base = float(item.get("precio_base", 0))
        except (TypeError, ValueError):
            return Response(
                {"error": "precio_base inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tipo = item.get("tipo_cliente", "GENERAL")
        descuento_pct = DESCUENTOS.get(tipo)
        if descuento_pct is None:
            return Response(
                {"error": f"tipo_cliente inválido: {tipo}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        precio_final = round(precio_base * (1 - descuento_pct / 100), 2)
        total += precio_final

        detalle.append({
            "precio_base": precio_base,
            "tipo_cliente": tipo,
            "descuento_pct": descuento_pct,
            "precio_final": precio_final,
        })

    return Response({"total": round(total, 2), "detalle": detalle})


@api_view(["GET"])
@permission_classes([AllowAny])
def programar_sala(request):
    try:
        asientos_disponibles = int(request.query_params.get("asientos_disponibles", 0))
    except (TypeError, ValueError):
        return Response(
            {"error": "asientos_disponibles debe ser un número entero"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    discapacidades_str = request.query_params.get("discapacidades", "")
    if not discapacidades_str.strip():
        return Response(
            {"error": "discapacidades es requerido (ej: 5,3,2)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        capacidades = [int(x.strip()) for x in discapacidades_str.split(",")]
    except (TypeError, ValueError):
        return Response(
            {"error": "discapacidades debe ser una cadena de números separados por coma"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    acumulado = 0
    indice = 0
    funciones_programadas = []

    while indice < len(capacidades):
        capacidad_actual = capacidades[indice]
        if acumulado + capacidad_actual <= asientos_disponibles:
            funciones_programadas.append({
                "funcion": indice + 1,
                "asientos": capacidad_actual,
            })
            acumulado += capacidad_actual
            indice += 1
        else:
            break

    asientos_libres = asientos_disponibles - acumulado

    return Response({
        "funciones_programadas": funciones_programadas,
        "asientos_libres": asientos_libres,
    })


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
