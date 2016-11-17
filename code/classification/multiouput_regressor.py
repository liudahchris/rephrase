from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.grid_search import GridSearchCV
import pandas as pd
import time

def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

def main():
    data_path = '../../classification_data/subset_data/{}'
    df = pd.read_csv(data_path.format('features_nov_17.csv'),index_col=0)
    target = pd.read_csv(data_path.format('lda_results.csv'),index_col=0)
    df = df.join(target)
    target_names = ['topic{}'.format(i) for i in xrange(1,19)]
    y = df[target_names].values
    X = df.drop(target_names,axis=1).values
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    # model = MultiOutputRegressor(RandomForestRegressor(n_estimators=500,max_depth=4))
    # model = RandomForestRegressor()
    # model.fit(X_train,y_train)
    # print model.predict(X_test)
    # print model.score(X_test,y_test)
    rf_params = {'n_estimators':[10,500,1000,1500,2000],'max_depth':[3,5,7,9,11,None]}
    start = time.time()
    print 'Running Grid Search...'
    gs = GridSearchCV(RandomForestRegressor(),rf_params,n_jobs=-1)
    gs.fit(X_train,y_train)
    end = time.time()
    print 'Grid Search Completed in {} seconds'.format(strtimedelta(start,end))
    best_model = gs.best_estimator_
    print gs.best_params_
    print best_model.score(X_test,y_test)


if __name__=='__main__':
    main()
