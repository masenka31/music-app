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
    if not ('chosen_artists' in context.keys()) or delete_cache:
        context['chosen_artists'] = []
        context['chosen_ids'] = []
        context['chosen_songs'] = []
        context['ready'] = False
        context['pasted'] = False
        request.session['send_input'] = []
        
    
    ## VYBÍRÁNÍ PÍSNIČEK Z DATABÁZE PŘI ZADÁNÍ UMĚLCE --------------------------------------------
    # pokud člověk zadá umělce, uloží se do art_name
    art_name = request.POST.get('art_name')
    if art_name:
        songList = sc.song_list2(data, art_name)
        context['pasted'] = True
        context['songList'] = songList
        context['art_name'] = art_name
        request.session['artist_name'] = art_name

    ## ULOŽENÍ PÍSNIČEK PŘI ZAKLIKÁNÍ V CHECKLISTU ------------------------------------------------
    chosen_ids = request.POST.getlist('checklist')
    chosen_tracks = sc.names_from_ids(data,chosen_ids)
    print(chosen_tracks)

    if chosen_ids:
        art_name = request.session.get('artist_name')
        context['chosen_artists'].append(art_name)
        context['chosenSongs'] = chosen_tracks
        context['ready'] = True
        context['pasted'] = False
        context['chosen_ids'].append(chosen_ids)
        context['chosen_songs'].append(chosen_tracks.values[:])
        print(context['chosen_songs'])
        context['song_name'] = chosen_tracks.values[0]

    # temporary files kvůli resetu na heroku
    # a taky kvůli manipulaci s daty
    # až na to, že to stále nefunguje :(
    tmp1 = []
    tmp1 = context['chosen_ids']
    input_ids = [item for sublist in tmp1 for item in sublist]
    tmp2 = []
    tmp2 = context['chosen_songs']
    input_songs = [item for sublist in tmp2 for item in sublist]
    tmp3 = []
    tmp3 = context['chosen_artists']
    input_artists = [item for item in tmp3]

    # input, který se posílá skrz django do další page -> knn

    send_input = {
        'artists': input_artists,#context['chosen_artists'],
        'songs': input_songs,
        'ids': input_ids,
    }
    request.session['send_input'] = send_input
    print(request.session['send_input'])

    # a jedeme view
    return render(request, 'model/checklist.html', context)

def knn(request):
    # context jako vždy
    context = pages
    # získání přeneseného inputu a uložení do lokálních proměnných
    sent_input = request.session.get('send_input')
    print(sent_input)
    input_ids = sent_input['ids']
    input_artists = sent_input['artists']
    input_songs = sent_input['songs']

    # recommentations
    recommended = knn_model.recommend_knn(input_ids, input_artists)
    #print(recommended)
    context['was_recommended'] = True # uložení do contextu
    rec_ids = recommended['track_id']
    rec_songs = recommended['track_name']
    rec_artists = recommended['artist_name']

    # zazipování, aby bylo možné data přenést do HTML
    context['input_songs'] = input_songs
    context['input_artists'] = input_artists
    recommended_list = zip(rec_ids, rec_songs, rec_artists)
    context['all'] = recommended_list

    return render(request, 'model/knn.html', context)

def model(request):
    data = sc.read_data()
    nm = request.POST.get('test')
    #n = request.POST.get('number') - TBD
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