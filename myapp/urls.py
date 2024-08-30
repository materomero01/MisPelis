from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name="index"),  #como solo tiene '' es la principal
    path('signup/',views.signup,name="signup"),
    path('login/',views.signin,name="login"),
    path('logout/',views.signout,name="logout"),
    path('about/',views.about,name="about"),
    path('peliculas/',views.peliculas,name="peliculas"),
    path('peliculas_user/',views.peliculas,name="peliculas_user"),
    path('peliculas/delete/<str:id>',views.delete_pelicula,name='delete_pelicula'),
    path('peliculas/mark_pelicula_vista/<str:id>',views.mark_pelicula_vista,name='mark_pelicula_vista'),
    path('peliculas/<str:id>',views.pelicula,name="pelicula_detail"),
    path('create_pelicula/', views.create_pelicula,name="create_pelicula"),
    path('debug',views.debug,name='debug')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)