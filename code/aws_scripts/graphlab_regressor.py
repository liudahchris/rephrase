import graphlab as gl
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

if __name__=='__main__':
    data_dir = '../data/classification/{}'
    sf = gl.SFrame(data_dir.format('regression_values_sframe.csv'))
    features = gl.SFrame(data_dir.format('aws_complete_features.csv'))
    sf = sf.join(features, on='track_id')
    del features

    train, test = sf.random_split(0.9)
    train = train.to_dataframe()
    y_train = train.pop('X1')
    rf = RandomForestRegressor(n_estimators=100,verbose=1)
    rf.fit(train,y_train)

    del train
    del y_train


    test = test.to_dataframe()
    y_test = test.pop('X1')
    rf.score(test,y_test)
