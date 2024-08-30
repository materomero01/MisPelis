from django.core.management.base import BaseCommand
from myapp.management.utils.cargar_pelis_func import cargar_peliculas

class Command(BaseCommand):
    help = 'Carga películas desde TMDb API'

    def handle(self, *args, **kwargs):
        cargar_peliculas()
        self.stdout.write(self.style.SUCCESS('Películas cargadas exitosamente.'))
