import graphlab as gl
import pandas as pd
import numpy as np
from collections import Counter

def load_sframe():
    path = 'https://s3-us-west-2.amazonaws.com/liudahchris/aws_complete_sframe_bow.csv'
    return gl.SFrame(path)

def majority_vote(s_arr):
    majority = []
    for row in s_arr:
        klass = Counter(row.values()).most_common(1)[0][0]
        majority.append(klass)
    return majority

def main():
    NUM_TOPICS=50
    NUM_ITERS=500
    sf = load_sframe()
    lda = gl.topic_model.create(sf['bag_of_words'],num_topics=NUM_TOPICS,\
                                num_iterations=NUM_ITERS)
    votes = gl.SFrame()
    for i in xrange(NUM_TOPICS+1):
        votes[str(i)] = lda.predict(sf['bag_of_words'])
    labels = majority_vote(votes)
    del votes
    sf['labels'] = labels

    FNAME = 'graphlab_labels.csv'
    sf[['track_id','labels']].save(FNAME)
