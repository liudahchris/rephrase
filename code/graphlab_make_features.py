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

def write_topics(topics,fname='topics.txt'):
    with open(fname,'w') as f:
        for i,row in enumerate(topics):
            f.write('topic {}: '.format(i)+str(row)+'\n')


def main():
    NUM_TOPICS=25
    NUM_ITERS=500
    sf = load_sframe()
    lda = gl.topic_model.create(sf['bag_of_words'],num_topics=NUM_TOPICS,\
                                num_iterations=NUM_ITERS)

    lda.save('lda_25topics')
    topics = lda.get_topics(output_type='topic_words',num_words=20)
    write_topics(topics,fname='topics_25.txt')

    NUM_VOTERS=100
    votes = gl.SFrame()
    for i in xrange(NUM_VOTERS):
        votes[str(i)] = lda.predict(sf['bag_of_words'])
    labels = majority_vote(votes)
    del votes

    sf['labels'] = labels
    # sf['probas'] = lda.predict(sf['bag_of_words'],output_type='probability')

    FNAME = 'graphlab_labels_25.csv'
    sf[['track_id','labels']].save(FNAME)

    # FNAME = 'graphlab_probas.csv'
    # sf[['track_id','probas']].save(FNAME)
