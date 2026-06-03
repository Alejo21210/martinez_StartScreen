from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"generos", views.GeneroViewSet)
router.register(r"peliculas", views.PeliculaViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("cine/entradas/", views.calcular_entradas, name="calcular-entradas"),
    path("cine/sala/", views.programar_sala, name="programar-sala"),
]
