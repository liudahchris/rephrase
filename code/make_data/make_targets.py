import pandas as pd
import numpy as np
import sqlite3
from nltk.corpus import stopwords
from unidecode import unidecode
from collections import Counter
import cPickle as pickle
from sklearn.decomposition import LatentDirichletAllocation as LDA

def drop_empty(df):
    '''Drops rows of data where values are all 0'''
    to_drop = []
    for ind in df.index:
        if df.loc[ind].sum()==0:
            to_drop.append(ind)
    return df.drop(to_drop)

def drop_stop_words(df):
    '''Drops columns of dataframe representing stopwords'''
    stop_words = stopwords.words('english') + stopwords.words('spanish') + \
                 stopwords.words('german') + stopwords.words('french')
    col_keep = []
    for word in df.columns:
        if word not in stop_words:
            col_keep.append(word)
    return df[col_keep]

def main():
    # Load and clean data
    path = '../data/aws_complete_bow.csv'
    df = pd.read_csv(path,index_col=0)
    # df = drop_empty(df)
    df = drop_stop_words(df)

    # Perform LDA
    n_topics = 15
    lda = LDA(n_topics=n,max_iter=30,learning_method='online',n_jobs=-1)

if __name__=='__main__':
    main()
