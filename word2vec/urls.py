from django.urls import path
from . import views # importing the file views.py

urlpatterns = [
    path('', views.w2v_main, name='w2v_main'),
    path('checklist/', views.w2v_checklist, name='w2v_checklist'),
    path('w2v_model/', views.w2v_model, name='w2v_model'),
]