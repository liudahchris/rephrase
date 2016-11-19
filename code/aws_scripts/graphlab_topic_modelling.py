import graphlab as gl

# import pandas as pd
import numpy as np
import sqlite3
from nltk.corpus import stopwords
from unidecode import unidecode
from collections import Counter
import cPickle as pickle
from sklearn.decomposition import LatentDirichletAllocation as LDA
import graphlab as gl
import pandas as pd

def s3_upload_string(bucket_name,data,fname):
    access_key, secret_access_key = get_aws_access()
    conn = boto.connect_s3(access_key, secret_access_key)
    if conn.lookup(bucket_name) is None:
        bucket = conn.create_bucket(bucket_name, policy='public-read')
    else:
        bucket = conn.get_bucket(bucket_name)
    key = bucket.new_key(fname)
    key.set_contents_from_string(data)

def write_description(lda,X,df,db_path):
    labels = np.argmax(X,axis=1)
    c = Counter(labels)
    desc = ""
    for k,v in c.iteritems():
        desc+="Topic {}: {}\n".format(k,v)
    desc+='\n'

    components = lda.components_
    word_mask = np.array([row[::-1] for row in np.argsort(components,axis=1)])[:,:10]
    filtered_words = np.array(df.columns)[word_mask]

    songs_mask = np.argsort(X,axis=0).T
    songs_mask = np.array([mask[::-1] for mask in songs_mask])[:,:5]
    imp_3track_ids = np.array(df.index)[songs_mask]

    conn = sqlite3.connect(db_path)
    q = "SELECT title, artist_name FROM songs WHERE track_id = '{}';"
    # q2 = "SELECT title, artist_name FROM songs WHERE track_id = 'TRAWVWS128F42ADCD1';"
    # print q.format(imp_track_ids[0])
    for topic_num, (track_ids, topic) in enumerate(zip(imp_3track_ids,filtered_words)):
        desc += "Topic {}\n".format(topic_num+1)
        desc += str(topic)+'\n'
        formatted = '\t"{}" by {}\n'
        for track_id in track_ids:
            song,artist= conn.execute(q.format(track_id)).fetchone()
            desc += formatted.format(unidecode(song), unidecode(artist), topic[0:5])
    conn.close()
    return desc

def pickle_object(something, name):
    with open('/home/ubuntu/{}.pkl'.format(name), 'w') as f:
        pickle.dump(something, f)
    return None

def main():
    BUCKETNAME = 'liudahchris'

    print "LOADING SFRAME..."
    sf = gl.SFrame(data='../data/aws_complete_sframe_bow.csv')
    print "LOADING COMPLETE"


    NUM_TOPICS = 7
    NUM_ITERS = 250
    model = gl.topic_model.create(dataset=sf['bag_of_words'],\
                                  num_topics=NUM_TOPICS,\
                                  num_iterations=NUM_ITERS,\
                                  method='alias',\
                                  beta=0.1)
    model.get_topics(output_type='topic_words').print_rows(num_rows=NUM_TOPICS)
    target = model.predict(df['bag_of_words'])
    # Perform LDA
    # N = 15
    # X,lda = train_lda(n_topics=N)
    # print "TRAINING MODEL..."
    # lda = LDA(n_topics=n_topics,learning_method='online',n_jobs=-1)
    # lda.fit(df)
    # print "TRAINING COMPLETE..."
    #
    # Write some descriptive results
    # DB_PATH='/home/ubuntu/project/data/track_metadata.db'
    # s3_upload_string(BUCKETNAME,write_description(lda,X,df,DB_PATH),'lda_description.txt')
    #
    # Generate and write target files
    # labels = np.argmax(X,axis=1)
    # labeled_df = pd.DataFrame(data=labels,index=df.index)
    # s3_upload_string(BUCKETNAME,labeled_df.to_csv(),'aws_classification_targets.csv')
    # del labeled_df
    #
    # composition_df = pd.DataFrame(data=X,index=df.index)
    # s3_upload_string(BUCKETNAME,labeled_df.to_csv(),'aws_lda_composition.csv')
    # del composition_df
    #
    # Save pickled model
    # pickle_object(lda,'lda')

if __name__=='__main__':
    main()
