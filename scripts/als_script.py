from ALS_MUSIC import ALSRecommender
import pandas as pd

def recommend_als(input_ids,k=10,disliked=None):
    reco = ALSRecommender(factors=30, regularization=0.1)
    reco.load_model(filename="data/ALS_trained_m.sav")
    rec_ids = reco.predict(input_ids,k,disliked_ids=disliked)
    return rec_ids.tolist()