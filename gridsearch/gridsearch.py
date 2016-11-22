import graphlab as gl


def load_data():
    d_path = '../data/classification/{}'
    features_path = d_path.format('aws_complete_features.csv')
    labels_path = d_path.format('graphlab_labels_25.csv')
    features = gl.SFrame(features_path)
    sf = gl.SFrame(labels_path)
    return sf.join(features,on='track_id')


def main():
    sf = load_data()
    train, test = sf.random_split(0.9)
    train, valid = train.random_split(0.8)

    params = {'target': 'labels',
             'class_weights': 'auto',
             'max_depth': [5,10,20,30,40,50],
             'max_iterations': [100,250,500,750,1000]
             }


    job = gl.grid_search.create((train,valid),
                                gl.boosted_trees_classifier.create,
                                params
                                )

    job.save('gbm_gridsearch')

if __name__=='__main__':
    main()
