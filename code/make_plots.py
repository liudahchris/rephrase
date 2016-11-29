import graphlab as gl
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    features = gl.SFrame('../classification_data/full_data/aws_complete_features.csv')
    sf = gl.SFrame('../classification_data/full_data/graphlab_labels_25.csv')
    return sf.join(features,on='track_id').remove_column('track_id')

def make_heatmap(sim,names=None,outname=None):
    ax = sns.heatmap(sim)
    if names is not None:
        ax.set_xticklabels(names,rotation=90)
        ax.set_yticklabels(names[::-1],rotation=0)
    plt.title('Cosine Similarity of Sound Features')
    plt.tight_layout()
    if outname:
        plt.save_fig(outname)
        return
    plt.show()
    return

def main():
    sf = load_data()
    y = sf['labels'].to_numpy()
    sf = sf.remove_column('labels')

    scaler = StandardScaler()
    X = scaler.fit_transform(sf.to_numpy())
    centers = []
    for i in xrange(25):
        mask = np.where(y==i)
        centers.append(X[mask].mean(axis=0))
    centers = np.array(centers)

    mask = np.array([0,1,2,3,7,16,17,19,23,10,15,22,24,8,\
                    10,15,22,24,8,11,13,14,21,20,18,4,5,6,9])
    sorted_centers = centers[mask]

    lda = gl.load_model('../lda_25topics')
    topics = lda.get_topics(output_type='topic_words')
    topic_names = []
    for topic in topics:
        topic_names.append(' '.join(topic['words']))

    topic_names = np.array(topic_names)[mask]

    sim = cosine_similarity(sorted_centers)
    make_heatmap(sim,topic_names)

if __name__=='__main__':
    main()
