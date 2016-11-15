import os
import sys
import glob
from collections import Counter,defaultdict
import time
import datetime
import pandas as pd

from setup_path import setup_path
setup_path()
import hdf5_getters as GETTERS

def apply_to_subset_files(basedir,func=lambda x: x,ext='.h5'):
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files:
            func(f)
    return cnt

def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

def main():
    df = pd.read_csv('../classification_data/subset_data/labeled_df.csv')
    tracks = df.track_id.values

    list_of_rows = []

    def func_to_get_track_data(filename):
        h5 = GETTERS.open_h5_file_read(filename)
        track_id = GETTERS.get_track_id(h5)
        funcs =[GETTERS.get_duration,
                GETTERS.get_key,
                GETTERS.get_loudness,
                GETTERS.get_mode,
                GETTERS.get_tempo,
                GETTERS.get_time_signature]
        if track_id in tracks:
            row_data = [track_id]
            for func in funcs:
                row_data.append(func(h5))
            list_of_rows.append(row_data)
        h5.close()
        return None

    t1 = time.time()
    apply_to_subset_files(msd_subset_data_path,func=func_to_get_track_data)
    t2 = time.time()
    print 'data extracted in:',strtimedelta(t1,t2)

    return list_of_rows

if __name__=='__main__':
    msd_subset_path='/Users/christopherliu/Desktop/projects/music_project/data/MillionSongSubset'
    msd_subset_data_path=os.path.join(msd_subset_path,'data')
    msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
    msd_code_path='/Users/christopherliu/Desktop/projects/music_project/helper_functions/MSongsDB'
    cols = ['track_id','duration','key','loudness','mode','tempo','time_sig']
    data = main()
