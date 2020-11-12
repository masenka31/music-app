from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise
import pickle
from sklearn import preprocessing


class KNNRecommender:
    def __init__(self):
        self.model = None
        self.data_sparse = None
        self.le = None

    def fit(self, data, save=False, filename=None):
        data["rating"] = 1.0  # add column with ratings
        data["rating"] = data["rating"].astype("float32")
        data = data.drop_duplicates(["track_id", "user_id"])  # remove duplicates

        self.le = preprocessing.LabelEncoder()
        self.le.fit(data["track_id"])

        wide_data = data.pivot(index="track_id", columns="user_id", values="rating").fillna(0)
        self.data_sparse = csr_matrix(wide_data.values)

        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model.fit(self.data_sparse)

        if save:
            if filename is None:
                filename = "KNN_trained_m.sav"
            pickle.dump(self, open(filename, 'wb'))

    def load_model(self, filename):
        with open(filename, "rb") as f:
            loaded_model = pickle.load(f)
            self.model = loaded_model.model
            self.data_sparse = loaded_model.data_sparse
            self.le = loaded_model.le

        del loaded_model

    def predict(self, input_ids, k, banned_ids=None):
        # now supports banning certain ids which the model shouldn't recommend (e.g. songs from the same artist)
        input_ids = list(set(input_ids) & set(self.le.classes_))  # filter inputs unseen during training
        if not input_ids:
            raise RuntimeError("None of the input ids are in the dataset.")

        input_ids_tr = self.le.transform(input_ids)

        distances, indices = self.model.kneighbors(self.data_sparse[input_ids_tr], n_neighbors=10*k)
        best = indices.flatten()
        best = list(set(best) - set(input_ids_tr))
        if banned_ids is not None:
            # filter banned ids to only those already seen by the LabelEncoder
            # otherwise it would raise ValueError
            banned_ids = list(set(banned_ids) & set(self.le.classes_))
            banned_ids_tr = self.le.transform(banned_ids)

            best = list(set(best) - set(banned_ids_tr))
            #print(best)
            if not best:
                #return "False"
                raise RuntimeError("Couldn't find any songs to recommend.")

        final_dist = dict.fromkeys(best, 0)
        for song_rec in best:
            for song_input in input_ids_tr:
                dist = float(pairwise.cosine_distances(self.data_sparse[song_rec], self.data_sparse[song_input]))
                final_dist[song_rec] += dist

        return self.le.inverse_transform(sorted(final_dist, key=final_dist.get)[0:k])
        # final_dist_tr = {self.le.inverse_transform(k): v for k, v in final_dist.items()}
        # final_dist_tr = {str(self.le.inverse_transform([k])[0]): v for k, v in final_dist.items()}
        # return sorted(final_dist_tr.items(), key=lambda x: x[1])