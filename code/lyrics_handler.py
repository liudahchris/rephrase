import numpy as np
import pandas as pd
import sqlite3

def write_to_csv():
    path = '../data/lyrics/data/{}'
    conn = sqlite3.connect(path.format('mxm_dataset.db'))
    with open(path.format('vocab.txt')) as f:
        cols = f.read().split(',')
    # q = 'SELECT DISTINCT track_id FROM lyrics;'
    # tracks = [track[0] for track in conn.execute(q).fetchall()]

    with open(path.format('../metadata/subset_with_lyrics.csv')) as f:
        subset_with_lyrics = f.read().split()
    q = "SELECT word, count FROM lyrics WHERE track_id='{}';"
    df = pd.DataFrame(data=np.zeros((len(subset_with_lyrics),len(cols))),\
                        index=subset_with_lyrics,columns=cols)

    for track in subset_with_lyrics:
        q_ = q.format(track)
        word_counts = conn.execute(q_).fetchall()
        for word,count in word_counts:
            df.loc[track][word] = count
    conn.close()
    # out = path.format('subset_bow.csv')
    # df.to_csv(out)

def complete_to_csv():
    path = '../data/lyrics/data/{}'
    conn = sqlite3.connect(path.format('mxm_dataset.db'))
    with open(path.format('vocab.txt')) as f:
        cols = f.read().split(',')
    q = 'SELECT DISTINCT track_id FROM lyrics;'
    tracks = [track[0] for track in conn.execute(q).fetchall()]

    # with open(path.format('../metadata/subset_with_lyrics.csv')) as f:
    #     subset_with_lyrics = f.read().split()
    q = "SELECT word, count FROM lyrics WHERE track_id='{}';"
    df = pd.DataFrame(data=np.zeros((len(tracks),len(cols))),\
                        index=tracks,columns=cols)

    for track in tracks:
        q_ = q.format(track)
        word_counts = conn.execute(q_).fetchall()
        for word,count in word_counts:
            df.loc[track][word] = count
    conn.close()
    out = path.format('complete_bow.csv')
    df.to_csv(out)
