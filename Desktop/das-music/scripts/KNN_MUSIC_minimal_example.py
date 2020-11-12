from KNN_MUSIC import KNNRecommender
import pandas as pd
# minimal example how to use the KNN recommender

data = pd.read_csv("../data/song_interactions++.csv", usecols=["track_id", "user_id"])

reco = KNNRecommender()

# reco.fit(data, save=True)

reco.load_model(filename="../data/KNN_trained_m.sav")
songs = pd.read_csv("../data/song_info++.csv", usecols=["track_id", "artist_name", "track_name", "genre"])

banned_ids = songs[songs["artist_name"].isin(["Kanye West", "Kendrick Lamar"])]
banned_ids = banned_ids["track_id"].values

recommended_ids = reco.predict(["5VzeI5JM2y9t21JwrWAnkH", "7Ks4VCY1wFebnOdJrM13t6"], 10, banned_ids)
print(recommended_ids)
rec_songs = songs[songs["track_id"].isin(recommended_ids)]
pd.set_option('display.max_columns', None)
print(rec_songs)
