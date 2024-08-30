from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os

# Create your models here.

class Peliculas(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    genere = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    popularity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    def __str__(self):
        return self.name+' - '+self.description
    

class Pelicula_vista(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Peliculas, on_delete=models.CASCADE)
    vista = models.BooleanField(default=False)



