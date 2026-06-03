from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"generos", views.GeneroViewSet)
router.register(r"peliculas", views.PeliculaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
