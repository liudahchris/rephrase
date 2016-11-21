import graphlab as gl
import pandas as pd

if __name__=='__main__':
    data_dir = '../data/classification/{}'
    sf = gl.SFrame(data_dir.format('regression_values_sframe.csv'))
    features = gl.SFrame(data_dir.format('aws_complete_features.csv'))
    sf = sf.join(features, on='track_id')
    del features

    train, test = gl.random_split(0.9)
    train = train.to_dataframe()
    y_train = train.pop('labels')
    
