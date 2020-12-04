from django.urls import path
from . import views # importing the file views.py

urlpatterns = [
    path('checklist/',views.checklist,name='checklist'),
    path('recommendations/',views.recommendations,name='recommendations'),
    path('slider/',views.slider,name='slider')
]