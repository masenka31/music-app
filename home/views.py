from django.shortcuts import render  # useful shortcuts :)

pages = {
        'title': 'AI.Music',
        'home': 'Home',
        'random': 'Random Model',
        'knn': 'KNN Model',
        'w2v': 'Word2Vec',
        'als': 'ALS Model',
        'slider': 'Surprise',
        'about': 'Our Story',
}


# Create your views here.

def about(request):
    return render(request, 'home/about.html', pages)

def index(request):
    return render(request, 'home/index.html', pages)

def elements(request):
    return render(request, 'home/elements.html', pages)


def spotify(request):
    if request.method == 'POST':
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials

        # 'spotify:artist:6s22t5Y3prQHyaHWUN1R1C'

        artist_uri = request.POST.get('URI')
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id='7528f020f81f4206b11e46049dc0d977', client_secret='93118fc2de39497884c51419d51fe23d'))
        results = spotify.artist_top_tracks(artist_uri)
        final_results = results['tracks'][:10]
        artist_url = final_results[0]['artists'][0]['uri'][15:]

        reload_spotify = {
            'title': 'Know Your Music',
            'main': 'About',
            'first': 'Add Songs To Playlist',
            'second': 'Autocomplete',
            'third': 'Our Story',
            'fourth': 'Spotify',
            'results': final_results,
            'artist': artist_url
        }

        return render(request, 'home/spotify.html', reload_spotify)
    else:
        return render(request, 'home/spotify.html', pages)
