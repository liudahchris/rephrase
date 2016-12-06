import graphlab as gl
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import math

def load_data():
    features = gl.SFrame('../classification_data/full_data/aws_complete_features.csv')
    sf = gl.SFrame('../classification_data/full_data/graphlab_labels_25.csv')
    return sf.join(features,on='track_id').remove_column('track_id')

def make_heatmap(sim,names=None,outname=None):
    fig = plt.figure()
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

def sound_similarity_plot(centers,mask=None,outname=None):
    topic_names = np.array(['Nature','Music','French', 'Love in the Night',\
                    'Pain/Death', 'Protest','Party','Dream',\
                    'Spanish','Desire','Heartbreak','Courting',\
                    'Regret/Past','Time','German','Growing Up',\
                    'Italian','Falling in Love','Gangster Rap',\
                    'Other','Aggression','Trust/Distrust',\
                    'Departure','Religion','Exploration'])
    if mask:
        topic_names = topic_names[mask]
        centers = centers[mask]

    sim = cosine_similarity(centers)
    make_heatmap(sim=sim,names=topic_names,outname=outname)

def get_topics():
    lda = gl.load_model('../lda_25topics')
    topics = lda.get_topics(output_type='topic_words')
    topic_names = []
    for topic in topics:
        topic_names.append(' '.join(topic['words']))
    return topic_names

def normalized_centers(X,y):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    centers = []
    for i in xrange(len(np.unique(y))):
        mask = np.where(y==i)
        centers.append(X[mask].mean(axis=0))
    return np.array(centers)


def make_distribution():
    '../classification_data/full_data/y_test.txt'

def main():
    sf = load_data()
    y = sf['labels'].to_numpy()
    sf = sf.remove_column('labels')

    scaler = StandardScaler()
    X = scaler.fit_transform(sf.to_numpy())
    centers = normalized_centers(X,y)

    mask = [0,1,2,3,7,16,17,19,23,10,15,22,24,8,\
            11,13,14,21,20,18,4,5,6,9]

    # mask = [0,1,16,15,8,14,18]
    sound_similarity_plot(centers,mask)

if __name__=='__main__':
    main()
