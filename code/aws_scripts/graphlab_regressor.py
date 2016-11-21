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
    y_train = train['X1'].to_numpy()
    train.remove_columns(['track_id','X1'])
    train = train.to_dataframe().fillna(-1000)
    rf = RandomForestRegressor(n_estimators=100,verbose=1)
    rf.fit(train,y_train)

    del train
    del y_train

    y_test = test['X1'].to_numpy()
    test.remove_columns(['track_id','X1'])
    test = test.to_dataframe().fillna(-1000)
    rf.score(test,y_test)
