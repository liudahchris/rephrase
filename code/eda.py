from setup_path import setup_path
setup_path()
import hdf5_getters as GETTERS
import os
import sys
import glob
from collections import Counter,defaultdict
import time
import datetime
import pandas as pd

def apply_to_all_files(basedir,func=lambda x: x,ext='.h5'):
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files :
            func(f)
    return cnt


def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

def get_stuff():
    # all_tags = set()
    all_tags = defaultdict(int)
    def func_to_get_tags(filename):
        """
        This function does 3 simple things:
        - open the song file
        - get artist ID and put it
        - close the file
        """
        h5 = GETTERS.open_h5_file_read(filename)
        tags = GETTERS.get_artist_mbtags(h5)
        for tag in tags:
            all_tags[tag]+=1
        h5.close()


    t1 = time.time()
    apply_to_all_files(msd_subset_data_path,func=func_to_get_tags)
    t2 = time.time()
    print 'all artist names extracted in:',strtimedelta(t1,t2)

    classical = defaultdict(dict)
    def func_to_get_instrumental(filename):
        h5 = GETTERS.open_h5_file_read(filename)
        tags = set(GETTERS.get_artist_mbtags(h5))
        genres = {'classical','orchestral'}
        if tags.intersection(genres):
            d = {}
            d['artist'] = GETTERS.get_artist_name(h5)
            d['title'] = GETTERS.get_title(h5)
            song_id = GETTERS.get_song_id(h5)
            classical[song_id] = d
        h5.close()

    t1 = time.time()
    apply_to_all_files(msd_subset_data_path,func=func_to_get_instrumental)
    t2 = time.time()
    print 'all artist names extracted in:',strtimedelta(t1,t2)

def lyric_stuff():
    subset_ids = set()
    def func_to_get_track_ids(filename):
        h5 = GETTERS.open_h5_file_read(filename)
        id_ = GETTERS.get_track_id(h5)
        subset_ids.add(id_)
        h5.close()
    t1 = time.time()
    apply_to_all_files(msd_subset_data_path,func=func_to_get_track_ids)
    t2 = time.time()
    print 'task completed in:',strtimedelta(t1,t2)
    lyric_ids = set(pd.read_csv('../data/lyric_ids.csv').values.flatten())
    return len(subset_ids.intersection(lyric_ids))

def subset_with_lyrics_eda():
    with open('../data/subset_with_lyrics.csv') as f:
        ids = f.read().split()
    all_tags = defaultdict(int)
    def func_to_get_tags(filename):
        """
        This function does 3 simple things:
        - open the song file
        - get artist ID and put it
        - close the file
        """
        h5 = GETTERS.open_h5_file_read(filename)
        track_id = GETTERS.get_track_id(h5)
        tags = GETTERS.get_artist_mbtags(h5)
        if track_id in ids:
            for tag in tags:
                all_tags[tag]+=1
        h5.close()
    t1 = time.time()
    apply_to_all_files(msd_subset_data_path,func=func_to_get_tags)
    t2 = time.time()
    print 'task completed in:',strtimedelta(t1,t2)



if __name__=='__main__':
    msd_subset_path='/Users/christopherliu/Desktop/projects/music_project/data/MillionSongSubset'
    msd_subset_data_path=os.path.join(msd_subset_path,'data')
    msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
    msd_code_path='/Users/christopherliu/Desktop/projects/music_project/helper_functions/MSongsDB'
