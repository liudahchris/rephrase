import graphlab as gl


def load_data():
    d_path = '../data/classification/'
    features = gl.SFrame(d_path.format('aws_complete_features.csv'))
    sf = gl.SFrame(d_path.format('graphlab_labels_25.csv'))
    return sf.join(features,on='track_id')



train, test = gl.SFrame('')


params = {'target': 'labels',
         'class_weights': 'auto',
         'max_depth': [5,10,20,30,40,50],
         'max_iterations': [100,250,500,750,1000]
         }




job = gl.grid_search.create((train,valid),
                            gl.boosted_trees_classifier.create,
                            params
                            )

results =
