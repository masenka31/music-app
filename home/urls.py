from django.urls import path
from . import views # importing the file views.py

urlpatterns = [
    #path('', views.home, name='home-home'),
    path('about/', views.about, name='home-about'),
    path('', views.index, name='home-index'),
    path('spotify/', views.spotify, name='home-spotify'),
    path('elements/', views.elements, name='home-elements')
]