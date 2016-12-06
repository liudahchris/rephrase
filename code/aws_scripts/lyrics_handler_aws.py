import sqlite3
import graphlab
from nltk.corpus import stopwords

def complete_to_csv(f_out='sframe_bow.csv'):
    '''
    Extracts lyrics from sqlite database and saves it in Graphlab form.
    INPUT: Output file name
    OUTPUT: None
    '''
    stop_words = stopwords.words('english') + stopwords.words('spanish') + \
                 stopwords.words('german') + stopwords.words('french')

    path = '../../data/{}'
    conn = sqlite3.connect(path.format('mxm_dataset.db'))
    print 'Fetching Track IDs...'
    q = 'SELECT DISTINCT track_id FROM lyrics;'
    tracks = [track[0] for track in conn.execute(q).fetchall()]
    print 'Done fetching Track IDs'

    q = "SELECT word, count FROM lyrics WHERE track_id='{}';"
    sf = graphlab.SFrame()

    print 'Writing to SFrame...'
    for i,track in enumerate(tracks):
        q_ = q.format(track)
        word_counts = conn.execute(q_).fetchall()
        filtered = []
        for word, count in word_counts:
            if word not in stop_words:
                filtered.append((word,count))
        word_count_dict = dict(filtered)
        temp_sf = graphlab.SFrame({'track_id':[track], 'bag_of_words':[word_count_dict]})
        sf = sf.append(temp_sf)
        if i%500==0: print '{} tracks completed'.format(i)
    conn.close()
    print 'Done writing to Frame'
    print 'Saving to disk...'
    out = path.format(f_out)
    sf.save(out)
    print 'Complete'
    return

if __name__=='__main__':
    complete_to_csv()
