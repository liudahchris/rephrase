import os
import sys
import glob
from collections import Counter,defaultdict
import time
import datetime
import pandas as pd
import numpy as np
import sqlite3
import boto

msd_code_path='/home/ubuntu/project/helper_functions/MSongsDB'
assert os.path.isdir(msd_code_path),'wrong path' # sanity check
sys.path.append( os.path.join(msd_code_path,'PythonSrc') )
import hdf5_getters as GETTERS

def condense_segments(arr,new_size=4):
    '''Condense or inflate segments so each song has same number of segments'''
    if arr.shape[0]>=new_size:
        div = arr.shape[0]/new_size
        new_arr = []
        for i in xrange(new_size):
            new_arr.append(np.mean(arr[i*div:(i+1)*div],axis=0))
    elif arr.shape[0] < new_size:
        expand = new_size/arr.shape[0]
        new_arr = []
        for subarr in arr:
            if type(subarr)==np.ndarray:
                subarr = subarr[np.newaxis,:]
            new_arr+=(list(np.repeat(subarr,expand,axis=0)))
        if np.array(new_arr).shape[0] < new_size:
            num_rows_to_add = new_size - np.array(new_arr).shape[0]
            new_arr+=(list(np.repeat(arr[-1],num_rows_to_add,axis=0)))
    else:
        return arr.flatten()
    return list(np.array(new_arr).flatten())

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

def make_data(num_segments=4):
    path = '../lyrics/{}'
    conn = sqlite3.connect(path.format('mxm_dataset.db'))
    print 'Fetching Track IDs...'
    q = 'SELECT DISTINCT track_id FROM lyrics;'
    tracks = [track[0] for track in conn.execute(q).fetchall()]
    print 'Done fetching Track IDs'
    conn.close()
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
                row_data+=condense_segments(segment_mat,new_size=num_segments)
            list_of_rows.append(row_data)
        h5.close()
        return None

    t1 = time.time()
    apply_to_subset_files(msd_subset_data_path,func=func_to_get_track_data)
    t2 = time.time()
    print 'data extracted in:',strtimedelta(t1,t2)

    return list_of_rows

def make_segment_cols(colname,num_vals,num_segments=4):
    s = 'seg{}'+colname+'{}'
    return [s.format(i,j) for i in range(1,num_segments+1) for j in range(1,num_vals+1)]

def get_aws_access():
    return os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_ACCESS_KEY']

def s3_upload_file(bucketname,data,fname='aws_features.csv'):
    access_key, secret_access_key = get_aws_access()
    conn = boto.connect_s3(access_key, secret_access_key)
    if conn.lookup(bucket_name) is None:
        bucket = conn.create_bucket(bucket_name, policy='public-read')
    else:
        bucket = conn.get_bucket(bucket_name)
    key = bucket.new_key(fname)
    key.set_contents_fromstring(data.to_csv())

if __name__=='__main__':
    NUM_SEGMENTS = 4

    msd_subset_path='/mnt/snap/'
    msd_subset_data_path=os.path.join(msd_subset_path,'data')
    msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
    msd_code_path='/home/ubuntu/project/helper_functions/MSongsDB'
    segment_data = [('pitch',12),('timbre',12),('loudness',1),('loudness_time',1)]
    cols = ['track_id','duration','key','loudness','mode','tempo','time_sig']
    for feat,num in segment_data:
        cols+=make_segment_cols(feat,num,NUM_SEGMENTS)
    data = make_data(NUM_SEGMENTS)
    df = pd.DataFrame(data=data,columns=cols).set_index('track_id')
    del data

    bucket_name = 'liudahchris'
    s3_upload_file(bucket_name,df)
