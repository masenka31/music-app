from django.urls import path
from . import views # importing the file views.py

urlpatterns = [
    path('', views.model, name='model'),
    path('checklist/', views.checklist, name='checklist'),
    path('knn/', views.knn, name='knn'),
]