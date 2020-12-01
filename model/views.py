from django.shortcuts import render
import sys
import os
new_path = os.path.dirname(os.path.realpath(__file__)) + '/../scripts/'
sys.path.append(new_path)
import test_script as sc
import knn_script as knn_model
import w2v as wv
import pandas as pd
from json import dumps


pages = {
        'title': 'Know Your Music',
        'home': 'Home',
        'random': 'Random Model',
        'knn': 'KNN Model',
        'w2v': 'Word2Vec',
        'about': 'Our Story',
}


# Create your views here.

def knn(request):
    # context jako vždy
    context = pages

    # a render...
    return render(request, 'model/knn.html', context)

def random(request):
    data = sc.read_data()
    nm = request.POST.get('test')
    if nm:
        n = 10
        how_many, rand_sample = sc.find_artist(nm,data,n)
        values = rand_sample.values

    context = pages
    if nm:
        context['name'] = nm
        context['number'] = how_many
        context['values'] = values

    return render(request, 'model/random.html', context)

def word2vec(request):
    context = pages
    return render(request,'model/word2vec.html',context)

def als(request):
    context = pages
    return render(request, 'model/als.html', context)