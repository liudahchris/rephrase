import graphlab as gl
from sklearn.ensemble import RandomForestClassifier

def load_data():
    features_path = 'https://s3-us-west-2.amazonaws.com/liudahchris/aws_complete_features.csv'
    labels_path = 'https://s3-us-west-2.amazonaws.com/liudahchris/graphlab_labels.csv'
    features = gl.SFrame(features_path)
    sf = gl.SFrame(labels_path)
    return sf.join(features,on='track_id')

def make_model():
    sf = load_data()
    # model = gl.classifier.create(sf,target='labels')
    train, test = sf.random_split(0.9)
    model = gl.random_forest_classifier.create(train,target='labels')

    results = model.evaluate(test)


if __name__=='__main__':
    sf = load_data()
    model = gl.classifier.create(sf,target='labels')
