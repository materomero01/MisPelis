import requests
from django.core.files import File
from django.core.files.base import ContentFile
from myapp.models import Peliculas
from django.conf import settings
import os
from decimal import Decimal
def cargar_peliculas():
    url = 'https://api.themoviedb.org/3/movie/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'es-MX',  # MX porque es mejor los títulos en español
        'page': 2  # Especifica que solo se desea la primera página
    }

    response = requests.get(url, params=params)
    data = response.json()
    movies_count = 1

    for movie in data.get('results', []):
        if movies_count >= 20:
            break

        titulo_original = movie.get('original_title')
        descripcion = movie.get('overview')
        imagen = movie.get('poster_path')

        # Obtener los detalles de la película para extraer los géneros
        movie_id = movie['id']
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        details_params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'es-MX'
        }
        details_response = requests.get(details_url, params=details_params)
        details_data = details_response.json()
        generos = [genero['name'] for genero in details_data.get('genres', [])]
        genero = ', '.join(generos)
        popularity = details_data.get('vote_average')
        print(popularity)

        # Verificar si la película ya existe
        pelicula_existente = Peliculas.objects.filter(name=titulo_original).first()
        if pelicula_existente:
            print(f'La película "{titulo_original}" ya existe. Se omite.')
            continue

        print(f'Creando película: {titulo_original}')
        pelicula = Peliculas.objects.create(
            name=titulo_original,
            description=descripcion,
            genere=genero,
            popularity = Decimal(round(popularity, 1))
        )
        print('Película creada exitosamente')

        if imagen:
            print('Guardando imagen')
            img_url = f'https://image.tmdb.org/t/p/w500{imagen}'
            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                name = f"{titulo_original}.jpg"
                pelicula.image.save(name, ContentFile(img_response.content))
                pelicula.save()
                print('Imagen insertada correctamente')
            else:
                print(f'Error al descargar la imagen: {img_response.status_code}')

        print(f'Ya pusimos {movies_count} películas')
        movies_count += 1