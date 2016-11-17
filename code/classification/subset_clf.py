import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV

def main():
    data_path = '../../classification_data/subset_data/{}'
    # fname = 'subset_features.csv'
    fname = 'features_nov_16.csv'
    df = pd.read_csv(data_path.format(fname),index_col=0)
    label = pd.read_csv(data_path.format('labeled_df.csv'),index_col=0)
    df = df.join(label)
    df['key'] = df.key.apply(str)
    df = pd.get_dummies(df,'key')
    y = df.pop('label').values
    X = df.values
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    rf = RandomForestClassifier(n_estimators=500,max_depth=10,n_jobs=-1)
    rf.fit(X_train,y_train)
    print rf.predict_proba(X_test)
    print Counter(rf.predict(X_test))
    print Counter(y_test)
    print rf.score(X_test,y_test)
    # rf_params = {'n_estimators':[10,500,1000,1500,2000],'max_depth':[3,5,7,9,11,None]}
    # print 'Running Grid Search...'
    # gs = GridSearchCV(RandomForestClassifier(),rf_params)
    # gs.fit(X_train,y_train)
    # best_model = gs.best_estimator_
    # print gs.best_params_
    # print best_model.score(X_test,y_test)


if __name__=='__main__':
    main()
