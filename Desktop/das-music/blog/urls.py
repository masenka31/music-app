from django.urls import path
from . import views # importing the file views.py

urlpatterns = [
    #path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('', views.index, name='blog-index'),
    path('spotify/', views.spotify, name='blog-spotify'),
    path('elements/', views.elements, name='blog-elements')
]