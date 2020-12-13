from django.urls import path
from . import views # importing the file views.py

urlpatterns = [
    path('random/', views.random, name='random'),
    path('knn/', views.knn, name='knn'),
    path('word2vec/',views.word2vec,name="word2vec"),
    path('als/',views.als,name="als"),
]