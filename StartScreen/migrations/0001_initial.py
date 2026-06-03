from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genero",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Pelicula",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=200)),
                ("codigo", models.CharField(max_length=50, unique=True)),
                ("duracion_minutos", models.PositiveIntegerField()),
                (
                    "precio_entrada",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("en_cartelera", models.BooleanField(default=True)),
                (
                    "genero",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="peliculas",
                        to="StartScreen.genero",
                    ),
                ),
            ],
        ),
    ]
