from gensim.models import KeyedVectors
""" www=KeyedVectors.load("../data/model.model", mmap='r')
def stat(lst):
    lst=www.most_similar(positive=lst,topn=20)
    for i in lst:
        print(i[0])
        
masa_list=["4MflGTO2ZTcSQ12bWcyRgI","4wTChU0tU44TAMC0xcQizi","19cL3SOKpwnwoKkII7U3Wh","3DamFFqW32WihKkTVlwTYQ",
           "7lGKEWMXVWWTt3X71Bv44I","5Hroj5K7vLpIG4FNCRIjbP","5ChkMS8OtdzJeqyybCc9R5","7EsjkelQuoUlJXEw7SeVV4",
           "5SHOb5hvMDzmIRfDhwBoq5","2PtBhfoPZ6VYtXkrE5FrCH","5aujQJTfXsWhLwqtmenKZ2",
           "7w87IxuO7BDcJ3YUqCyMTT"]
 
stat(masa_list) """

w2v_model = KeyedVectors.load("data/model.model", mmap='r')

def w2v_recommend(ids,n=10):
    w2v_model = KeyedVectors.load("data/model.model", mmap='r')
    rec = w2v_model.most_similar(positive=ids, topn=n)
    rec_ids = [i[0] for i in rec]
    #ratings = [i[1] for i in rec]
    return rec_ids#, ratings

""" def w2v_recommend(ids,w2v_model,n=10):
    rec = w2v_model.most_similar(positive=ids, topn=n)
    rec_ids = [i[0] for i in rec]
    #ratings = [i[1] for i in rec]
    return rec_ids#, ratings """

# slider from 0-1
def surprise_w2v(ids,slider,w2v_model,n=10):
    value = round(slider,2)*100
    rec_ids = w2v_recommend(ids,w2v_model,n+value)
    rec_ids = rec_ids[value:]
    return rec_ids

