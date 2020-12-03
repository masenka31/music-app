from scipy.sparse import csr_matrix
from sklearn import preprocessing
import implicit
import numpy as np
import pickle
import pandas as pd



class ALSRecommender:
    def __init__(self, factors=50, regularization=0.01, iterations=15):
        self.data_sparse = None
        self.le = None
        self.model = None
        self.factors = factors
        self.regularization = regularization
        self.iterations = iterations

    def fit(self, data, save=False, filename=None):
        data["rating"] = 1.0  # add column with ratings
        data["rating"] = data["rating"].astype("float32")
        data = data.drop_duplicates(["track_id", "user_id"])  # remove duplicates

        self.le = preprocessing.LabelEncoder()
        self.le.fit(data["track_id"])

        chunk_size = 5000
        chunks = [x for x in range(0, data.shape[0], chunk_size)]
        new_df = pd.concat([data.iloc[ chunks[i]:chunks[i + 1] - 1 ].pivot(index='track_id', columns='user_id', values='rating') for i in range(0, len(chunks) - 1)])

        #wide_data = data.pivot(index="track_id", columns="user_id", values="rating").fillna(0)
        wide_data = new_df.fillna(0)
        self.data_sparse = csr_matrix(wide_data.values)

        self.model = implicit.als.AlternatingLeastSquares(factors=self.factors, regularization=self.regularization,
                                                          iterations=self.iterations)
        self.model.fit(self.data_sparse)

        if save:
            if filename is None:
                filename = "ALS_trained_m.sav"
            pickle.dump(self, open(filename, 'wb'))

    def refit(self, factors=50, regularization=0.01, iterations=15):
        # keep the sparse matrix, but retrain the model with different parameters
        # creating the sparse matrix takes a lot longer than training itself
        self.factors = factors
        self.regularization = regularization
        self.iterations = iterations

        self.model = implicit.als.AlternatingLeastSquares(factors=self.factors, regularization=self.regularization,
                                                          iterations=self.iterations)
        self.model.fit(self.data_sparse)

    def load_model(self, filename):
        with open(filename, "rb") as f:
            loaded_model = pickle.load(f)
            self.model = loaded_model.model
            self.data_sparse = loaded_model.data_sparse
            self.le = loaded_model.le

        del loaded_model

    def predict(self, input_ids, k, banned_ids=None, disliked_ids=None):
        if k == "all":
            k = len(self.le.classes_)

        input_ids = list(set(input_ids) & set(self.le.classes_))  # filter inputs unseen during training
        if not input_ids:
            raise RuntimeError("None of the input ids are in the dataset.")

        if banned_ids is not None:
            banned_ids = list(set(banned_ids) & set(self.le.classes_))
            banned_ids_tr = self.le.transform(banned_ids)
        else:
            banned_ids_tr = []

        if disliked_ids is not None:
            disliked_ids = list(set(disliked_ids) & set(self.le.classes_))
            disliked_ids_tr = self.le.transform(disliked_ids)
        else:
            disliked_ids_tr = []

        input_ids_tr = self.le.transform(input_ids)
        user_input = np.zeros((len(self.le.classes_), 1))
        user_input[input_ids_tr] = 1
        user_input[disliked_ids_tr] = -100

        recs = self.model.recommend(0, csr_matrix(user_input.T), filter_already_liked_items=True,
                                    recalculate_user=True, N=k, filter_items=banned_ids_tr)
        recs = [x[0] for x in recs]
        return self.le.inverse_transform(recs)
