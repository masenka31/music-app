import math
from gensim.models import KeyedVectors
import pandas as pd

w2v_model = KeyedVectors.load("data/model202.model", mmap='r')

def model_pred(positive,negative=None,topn=20):
    lst=w2v_model.most_similar(positive=positive,negative=negative,topn=topn)
    return pd.DataFrame(lst,columns=["track_id","acc"]).iloc[:,[0]]



def pred(lst_user,df,interpret_keep=3,count=40,genre_keep=False,tempo_keep=False):
    df_pred=model_pred(lst_user,negative=None,topn=20)
    df_temp= df_pred.merge(df,on="track_id")
    ides=df_temp.drop_duplicates(subset='track_id').groupby('artist_name').head(interpret_keep).track_id.tolist()
    if not genre_keep:
        return df_temp[df_temp.track_id.isin(ides)]
    else:
        return crop(df_temp[df_temp.track_id.isin(ides)], genre_keep=genre_keep, tempo_keep=tempo_keep)



def crop(df_temp,genre_keep=False,tempo_keep=False):
    df_count=df_temp.groupby("track_id").count().loc[:,["genre"]].rename(columns={'genre':'ke'})
    df_temp=df_temp.join(df_count,on='track_id').sort_values(by="ke")
    df_temp=df_temp.groupby('genre').head(genre_keep)
    df_temp=df_temp.sort_index()
    df_temp=df_temp.drop_duplicates(subset="track_id")
    if(tempo_keep):
        df_temp=df_temp.groupby('tempo').head(tempo_keep)
    return df_temp



def predict_user_list(my_list,df,randomness=0):
    interpret_keep_list=[3,2,2,1,1]
    genre_keep_list=[False,4,3,2,1]
    tempo_keep_list=[False,False,False,4,2]
        
    return pred(my_list,df,
                interpret_keep=interpret_keep_list[randomness],count=4000,
                genre_keep=genre_keep_list[randomness],
                tempo_keep=tempo_keep_list[randomness]).drop_duplicates(subset="track_id").track_id.tolist()[:20]


def crop_slider(slider_value):
    slider = int(slider_value)
    index = math.ceil(slider/25)
    return index
