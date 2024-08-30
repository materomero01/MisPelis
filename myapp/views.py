from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from .models import Peliculas,Pelicula_vista
from .forms import CreateNewPelicula
import requests
from decouple import config
from django.conf import settings



def popularity_to_stars(popularity):
    if popularity < 0:
        popularity = 0
    elif popularity > 10:
        popularity = 10
    
    full_stars = int(popularity / 10 * 5)  # Número de estrellas llenas
    half_star = int((popularity % 10) / 10 * 2)  # 0 o 1 para media estrella
    empty_stars = 5 - full_stars - half_star  # Número de estrellas vacías
    print(full_stars,half_star,empty_stars)
    return {'full_stars': full_stars, 'half_star': half_star, 'empty_stars': empty_stars}

def debug(request):
    pelis = Peliculas.objects.order_by('-popularity')[:10]
    return render(request,'debug.html',{
        'pelis':pelis
    })

# Create your views here.
def index(request):
    pelis = Peliculas.objects.order_by('-popularity')[:10]
    return render(request,'index.html',{
        'pelis':pelis
    })

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('index')
            except Exception as e:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': str(e)
                })
        else:
            # Esto mostrará los errores generados por el formulario, como si el nombre de usuario ya existe
            return render(request, 'signup.html', {
                'form': form,
                'error': "Por favor, corrige los errores a continuación."
            })

def signin(request):
    if request.method == 'GET':
        return render(request,'login.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username= request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'login.html',{
            'form': AuthenticationForm,
            'error': "User or password is incorrect"
        })
        else:
            login(request,user)
            return redirect('index')

def signout(request):
    logout(request)
    return render(request,'index.html')

def about(request):
    username = "mateito"
    return render(request, 'about.html',{
        'username':username
    })

def peliculas(request):
    if request.user.is_authenticated:
        vistas = Pelicula_vista.objects.filter(user=request.user,vista=True).select_related('pelicula')
        pelis_vistas = [vista.pelicula for vista in vistas]
        pelis_no_vistas = Peliculas.objects.exclude(id__in=[peli.id for peli in pelis_vistas])
        pelis = pelis_vistas + list(pelis_no_vistas)
        pelis = sorted(pelis, key=lambda peli: peli.name)
        estrellas_pelis = {}
        
        for peli in pelis:
            popularity = peli.popularity
            stars = popularity_to_stars(popularity)
            estrellas_pelis[peli.id] = {
            'full_stars': '★' * stars['full_stars'],
            'half_star': '★' if stars['half_star'] else '',
            'empty_stars': '☆' * stars['empty_stars']
        }
        
        return render(request, 'peliculas_user.html', {
            'pelis': pelis,
            'pelis_vistas': pelis_vistas,
            'estrellas_pelis': estrellas_pelis
        })
    else:
        pelis = Peliculas.objects.all().order_by('name')
        estrellas_pelis = {}
        
        for peli in pelis:
            popularity = peli.popularity
            stars = popularity_to_stars(popularity)
            estrellas_pelis[peli.id] = {
            'full_stars': '★' * stars['full_stars'],
            'half_star': '★' if stars['half_star'] else '',
            'empty_stars': '☆' * stars['empty_stars']
        }
        return render(request, 'peliculas.html', {
            'pelis': pelis,
            'estrellas_pelis': estrellas_pelis
        })

def pelicula(request, id):
    if request.user.is_authenticated:
        vista = Pelicula_vista.objects.filter(pelicula=id,user=request.user).first()
        peli = get_object_or_404(Peliculas, id=id)
        stars = popularity_to_stars(peli.popularity)
        
        context = {
            'peli': peli,
            'stars': stars,
            'vista': vista,
            }

        if vista:
            context['vista'] = vista
        return render(request, 'pelicula_detail.html', context)
    else: 
        peli = get_object_or_404(Peliculas, id=id)
        stars = popularity_to_stars(peli.popularity)
        return render(request, 'pelicula_detail.html', {
            'peli': peli,
            'stars': stars
        })

@login_required
@permission_required('myapp.add_peliculas',raise_exception=True)
def create_pelicula(request): 
    if request.method == 'POST':
        form = CreateNewPelicula(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('peliculas')

    else:
        form = CreateNewPelicula()
        return render(request, 'create_pelicula.html',{
        'form':form
    })

@login_required
@permission_required('myapp.delete_peliculas',raise_exception=True)
def delete_pelicula(request,id): 
    peli = get_object_or_404(Peliculas,id=id)
    peli.delete()
    return redirect('peliculas')

@login_required
def mark_pelicula_vista(request,id):
    peli = get_object_or_404(Peliculas,id=id)
    vista, created = Pelicula_vista.objects.get_or_create(user=request.user, pelicula=peli)
    vista.vista = not vista.vista
    vista.save()
    previous_url= request.META.get('HTTP_REFERER','peliculas_user')
    return redirect(previous_url)

