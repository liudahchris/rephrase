import numpy as np
import graphlab as gl
import pandas as pd

def write_topics(topics,f_out='topics.txt'):
    """
    Writes topics iterable to text file.
    """
    with open(f_out,'w') as f:
        template = 'topic {}: {}\n'
        for i, topic in enumerate(topics):
            f.write(template.format(i,str(topic)))
    return


def main():
    '''
    Graphlab Topic Modelling
    Trains an LDA model on lyric data
    Saves 3 items to disk:
        1.) LDA Model
        2.) List of Topics (text file)
        3.) Predictions of the topic of songs
    '''
    print "LOADING SFRAME..."
    sf = gl.SFrame(data='../../data/sframe_bow.csv')
    print "LOADING COMPLETE"

    print "TRAINING LDA TOPIC MODEL..."
    NUM_TOPICS = 25
    NUM_ITERS = 500
    lda = gl.topic_model.create(dataset=sf['bag_of_words'],\
                                  num_topics=NUM_TOPICS,\
                                  num_iterations=NUM_ITERS
                                  )
    print "TRAINING COMPLETE"

    print "WRITING FILES TO DISK..."
    # SAVE LDA MODEL FOR FUTURE REFERENCE
    LDA_FILENAME = 'lda_{}_topics'
    lda.save(LDA_FILENAME.format(NUM_TOPICS))

    # SAVE TOPICS TO TXT FILE
    topics = lda.get_topics(output_type='topic_words',num_words=25)
    write_topics(topics)

    # PREDICT TOPIC OF SONGS
    composition = lda.predict(sf,output_type='probability').to_numpy()
    targets = np.argmax(composition,axis=1)
    F_OUT = 'song_targets.csv'
    with open(F_OUT,'w') as f:
        f.write('topic\n')
        for item in targets:
            f.write(item+'\n')
    return

if __name__=='__main__':
    main()
