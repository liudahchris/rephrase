import graphlab as gl
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def sklearn_regressor(sf):
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
    print rf.score(test,y_test)

if __name__=='__main__':
    data_dir = '../data/classification/{}'
    sf = gl.SFrame(data_dir.format('regression_values_sframe.csv'))
    features = gl.SFrame(data_dir.format('aws_complete_features.csv'))
    sf = sf.join(features, on='track_id')
    train,test = sf.random_split(0.9)

    train_regress_vals = train['X1'].to_numpy()
    train.remove_column('X1')
    test_regress_vals = test['X1'].to_numpy()
    test.remove_column('X1')

    del features
    del sf

    models = []
    preds = []
    for i in xrange(regression_values.shape[1]):
        train['target'] = train_regress_vals[:,i]
        model = sf.random_forest_regression.create(train,target='target')
        model.save('../models/model_{}'.format(i))
        # test['target'] = test_regress_vals[:,i]
        preds.append(model.predict(test).to_numpy())
    preds = np.array(preds).T
    np.savetxt('predicted_vals.txt',preds)
    np.savetxt('actual_vals.txt',test_regress_vals)
