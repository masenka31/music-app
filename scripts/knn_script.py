from KNN_MUSIC import KNNRecommender
import pandas as pd

# input ids as a vector like ["5VzeI5JM2y9t21JwrWAnkH", "7Ks4VCY1wFebnOdJrM13t6"]
# input artists as a vector like ["Kanye West", "Kendrick Lamar"]
# songs - the info dataset with
# usecols=["track_id", "artist_name", "track_name", "genre"]

def recommend_knn(input_ids, input_artists,prev_banned=[]):
    songs = pd.read_csv("data/song_info_v1.3.csv", usecols=["track_id", "artist_name", "track_name", "genre"])
    reco = KNNRecommender()
    reco.load_model(filename="data/KNN_trained_m.sav")

    banned_ids = songs[songs["artist_name"].isin(input_artists)]
    banned_ids = banned_ids["track_id"].values

    #if prev_banned:
    #    banned_ids.append(prev_banned)
    #    banned_ids = [item for sublist in banned_ids for item in sublist]

    recommended_ids = reco.predict(input_ids, 10, banned_ids)
    rec_songs = songs[songs["track_id"].isin(recommended_ids)]

    return rec_songs

def add_recommended(input_ids,input_artists,input_songs,rec_ids,rec_artists,rec_songs,likeList):
    banned = []
    for index in range(0,len(likeList)):
        if likeList[index] == 'true':
            print(rec_ids[index])
            print(rec_songs[index])
            input_ids.append(rec_ids[index])
            input_songs.append(rec_songs[index])
            tmp_art = rec_artists[index]
            if not tmp_art in input_artists:
                input_artists.append(tmp_art)
        if likeList[index] == 'banned':
            banned.append(rec_ids[index])

    return input_ids, input_artists, input_songs, banned