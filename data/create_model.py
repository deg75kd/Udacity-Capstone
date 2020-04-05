import sys
import os
import pandas as pd
import getpass
import pickle
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from myfunctions import tokenize

def load_data():
    """
    """
    # set database connection string
    DATABASE_URL = os.environ['DATABASE_URL']
    # print(DATABASE_URL)

    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    engine = create_engine(DATABASE_URL)
    print('engine created')

    selectQuery = 'select * from lyrics_table'
    lyrics_df = pd.read_sql(selectQuery, engine)

    return lyrics_df

def train_model(lyrics_df):
    """
    """
    genre_names = lyrics_df.groupby('genre').size().index.tolist()

    X = lyrics_df['lyrics']
    Y = lyrics_df['genre']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier())
    ])

    parameters = {
        'vect__max_df': (0.5, 1.0),
        'tfidf__use_idf': (True, False),
        'clf__n_estimators': [50, 100]
    }

    cv = GridSearchCV(pipeline,
                      param_grid = parameters,
                      n_jobs = 4,
                      cv = 3,
                      verbose = 5
    )
    cv.fit(X_train, Y_train)

    Y_pred = cv.predict(X_test)
    print(classification_report(Y_test, Y_pred))

    return cv

def export_model(cv, pickle_file):
    """
    """
    pickle_write = open('data/{}'.format(pickle_file), 'wb')
    pickle.dump(cv, pickle_write)
    print('Model saved to data/{}'.format(pickle_file))

    return None

def main():
    """
    """
    if len(sys.argv) == 2:
        pickle_file = sys.argv[1]
    
        lyrics_df = load_data()
        cv = train_model(lyrics_df)
        export_model(cv, pickle_file)

    else:
        print('You have passed in {} arguments.'.format(len(sys.argv)))
        print('Please provide the name of the pickle file to save.\n'\
              'Example: python create_model.py classifier.pkl')


if __name__ == '__main__':
    main()