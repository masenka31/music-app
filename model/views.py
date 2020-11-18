from django.shortcuts import render
import sys
import os
new_path = os.path.dirname(os.path.realpath(__file__)) + '/../scripts/'
sys.path.append(new_path)
import test_script as sc
import knn_script as knn_model
import pandas as pd
from json import dumps

pages = {
        'title': 'Know Your Music',
        'main': 'About',
        'first': 'Random Model',
        'second': 'KNN Model',
        'third': 'Our Story',
        'fourth': 'Spotify',
}

# Create your views here.

def checklist(request):
    ## ZÁKLADNÍ NAČTENÍ DAT ATD. ------------------------------------------------------
    # načtu data, vezmu si z nich unikátní umělce
    data = sc.read_data()
    artists = sc.artists_list(data)
    temp = artists.tolist()
    # uložení do JSONu pro JS
    # tohle vytváří artist list do JS pro autocomplete search
    art_list = dumps(temp)
    # a ještě si definuju context
    # přidám pages, které tam budou vždy
    context = pages
    # a JSON dump pro JS
    # tohle taky zůstane v contextu
    context['artists_autocomplete'] = art_list # tohle se posílá JS
    print(context.keys())
    context['keys'] = context.keys()
 
    ## RESET SONGŮ ----------------------------------------------------------------------
    # pokud od uživatele dostanu klik na tlačítko RESET
    delete_input = request.POST.get('delete_input')
    if delete_input:
        delete_cache = True
    else:
        delete_cache = False
    # globální proměnné, které se budou přenášet
    if not ('chosen_artists' in request.session.keys()) or delete_cache:
        request.session['chosen_artists'] = []
        request.session['chosen_ids'] = []
        request.session['chosen_songs'] = []
        if 'art_name' in request.session.keys():
            del request.session['art_name']
        # tohle zůstane v contextu, protože se to přenáší do HTML přímo
        context['ready'] = False
        context['pasted'] = False
    
    ## VYBÍRÁNÍ PÍSNIČEK Z DATABÁZE PŘI ZADÁNÍ UMĚLCE --------------------------------------------
    # pokud člověk zadá umělce, uloží se do art_name
    art_name = request.POST.get('art_name')
    context['art_name'] = art_name
    if art_name:
        songList = sc.song_list2(data, art_name)
        context['pasted'] = True        # tohle zůstává v contextu, aby bylo jasné, co chci nechat zobrazit
        context['songList'] = songList  # seznam písniček, které jdou do checklistu
        request.session['art_name'] = art_name  # aby bylo jasné, od jakého umělce bereme písničky

    ## ULOŽENÍ PÍSNIČEK PŘI ZAKLIKÁNÍ V CHECKLISTU ------------------------------------------------
    chosen_ids = request.POST.getlist('checklist')
    chosen_tracks = sc.names_from_ids(data,chosen_ids).tolist()

    if chosen_ids:
        art_name = request.session.get('art_name')
        request.session['chosen_artists'].append(art_name)
        # aby bylo jasné, co se má zobrazit
        context['ready'] = True
        context['pasted'] = False
        request.session['chosen_ids'].append(chosen_ids)
        request.session['chosen_songs'].append(chosen_tracks)

    context['chosen_songs'] = request.session.get('chosen_songs')
    if not context['chosen_songs']:
        context['ready'] = False
    else:
        context['ready'] = True
    # a jedeme view
    return render(request, 'model/checklist.html', context)

def knn(request):
    # context jako vždy
    context = pages
    # získání přeneseného inputu a uložení do lokálních proměnných
    ids = request.session.get('chosen_ids')
    input_artists = request.session.get('chosen_artists')
    songs = request.session.get('chosen_songs')

    # collect (kvůli blbé funkčnosti append)
    input_ids = [item for sublist in ids for item in sublist]
    input_songs = [item for sublist in songs for item in sublist]

    # pokud user dá like na písničky, vezmeme je a přidáme k předchozím
    likeList = request.POST.getlist('likeList')
    banned = []
    if likeList:
        #context['likeList'] = likeList
        rec_ids = request.session.get('rec_ids')
        rec_artists = request.session.get('rec_artists')
        rec_songs = request.session.get('rec_songs')
        input_ids, input_artists, input_songs, banned = knn_model.add_recommended(input_ids,input_artists,input_songs,rec_ids,rec_artists,rec_songs,likeList)
        
        print(len(input_ids))
        print(len(input_songs))

    # recommentations
    recommended = knn_model.recommend_knn(input_ids, input_artists)
    #recommended = knn_model.recommend_knn(input_ids, input_artists,banned)
    # uložení do listů
    rec_ids = recommended['track_id']
    rec_songs = recommended['track_name']
    rec_artists = recommended['artist_name']
    # uložení do kontextu pro výpis
    context['input_songs'] = input_songs
    context['input_artists'] = input_artists
    # zazipování, aby bylo možné data přenést do HTML
    # a uložení do kontextu
    recommended_list = zip(rec_ids, rec_songs, rec_artists)
    context['all'] = recommended_list

    # a ještě uložení do request.session, abychom mohli dávat nové recommendations
    request.session['rec_ids'] = rec_ids.tolist()
    request.session['rec_artists'] = rec_artists.tolist()
    request.session['rec_songs'] = rec_songs.tolist()
    # a uložení pro KNN?
    request.session['chosen_artists'] = input_artists
    request.session['chosen_ids'] = [input_ids]
    request.session['chosen_songs'] = [input_songs]

    # a render...
    return render(request, 'model/knn.html', context)

def model(request):
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

    return render(request, 'model/test.html', context)