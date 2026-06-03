from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .auth_views import register_view

router = DefaultRouter()
router.register(r"generos", views.GeneroViewSet)
router.register(r"peliculas", views.PeliculaViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("cine/entradas/", views.calcular_entradas, name="calcular-entradas"),
    path("cine/sala/", views.programar_sala, name="programar-sala"),
    path("auth/register/", register_view, name="auth-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
]
