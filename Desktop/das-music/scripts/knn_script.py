from KNN_MUSIC import KNNRecommender
import pandas as pd

# input ids as a vector like ["5VzeI5JM2y9t21JwrWAnkH", "7Ks4VCY1wFebnOdJrM13t6"]
# input artists as a vector like ["Kanye West", "Kendrick Lamar"]
# songs - the info dataset with
# usecols=["track_id", "artist_name", "track_name", "genre"]

def recommend_knn(input_ids, input_artists):
    songs = pd.read_csv("data/song_info_v1.3.csv", usecols=["track_id", "artist_name", "track_name", "genre"])
    reco = KNNRecommender()
    reco.load_model(filename="data/KNN_trained_m.sav")

    banned_ids = songs[songs["artist_name"].isin(input_artists)]
    banned_ids = banned_ids["track_id"].values

    recommended_ids = reco.predict(input_ids, 10, banned_ids)
    rec_songs = songs[songs["track_id"].isin(recommended_ids)]

    return rec_songs