import os
import sys
import glob
from collections import Counter,defaultdict
import time
import datetime
import pandas as pd
import numpy as np

from setup_path import setup_path
setup_path()
import hdf5_getters as GETTERS

def condense_segments(arr):
    div = arr.shape[0]/4
    averaged = []
    for i in xrange(4):
        averaged.append(np.mean(arr[i*div:(i+1)*div],axis=0))
    return list(np.array(averaged).flatten())

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
        segment_funcs = [GETTERS.get_segments_pitches,
                         GETTERS.get_segments_timbre,
                         GETTERS.get_segments_loudness_max,
                         GETTERS.get_segments_loudness_max_time]
        if track_id in tracks:
            row_data = [track_id]
            for func in funcs:
                row_data.append(func(h5))
            for func in segment_funcs:
                segment_mat = func(h5)
                row_data+=condense_segments(segment_mat)
            list_of_rows.append(row_data)
        h5.close()
        return None

    t1 = time.time()
    apply_to_subset_files(msd_subset_data_path,func=func_to_get_track_data)
    t2 = time.time()
    print 'data extracted in:',strtimedelta(t1,t2)

    return list_of_rows

def make_segment_cols(colname,num_vals):
    s = 'seg{}'+colname+'{}'
    return [s.format(i,j) for i in range(1,5) for j in range(1,num_vals+1)]


if __name__=='__main__':
    msd_subset_path='/Users/christopherliu/Desktop/projects/music_project/data/MillionSongSubset'
    msd_subset_data_path=os.path.join(msd_subset_path,'data')
    msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
    msd_code_path='/Users/christopherliu/Desktop/projects/music_project/helper_functions/MSongsDB'
    segment_data = [('pitch',12),('timbre',12),('loudness',1),('loudness_time',1)]
    cols = ['track_id','duration','key','loudness','mode','tempo','time_sig']
    for feat,num in segment_data:
        cols+=make_segment_cols(feat,num)
    data = main()
    df = pd.DataFrame(data=data,columns=cols).set_index('track_id')
    df.to_csv('features_nov_16.csv')
