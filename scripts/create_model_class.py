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

class Tokenizer():
    def __init__(self):
        self.pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer = tokenize)),
            ('tfidf', TfidfTransformer()),
            ('clf', RandomForestClassifier())
        ])
        self.parameters = {
            'vect__max_df': (0.5, 1.0),
            'tfidf__use_idf': (True, False),
            'clf__n_estimators': [50, 100]
        }
        self.n_jobs = 4
        self.cv = 3
        self.verbose = 5

cv = GridSearchCV(pipeline,
                          param_grid = parameters,
                          n_jobs = 4,
                          cv = 3,
                          verbose = 5
        )

    def tokenize(self, text):
        tokens = word_tokenize(text)
        lemmatizer = WordNetLemmatizer()
        
        clean_tokens = []
        for tok in tokens:
            clean_tok = lemmatizer.lemmatize(tok).lower().strip()
            clean_tokens.append(clean_tok)
            
        return clean_tokens

    def fit(self, X_train, Y_train):
        return self

	def predict(X_test):
        return None

    def transform(self, X):

        return pd.Series(X).apply(tokenize).values

def main():
    """
    """
    if len(sys.argv) == 2:
        pickle_file = sys.argv[1]
    
        # set database connection string
        DATABASE_URL = os.environ['DATABASE_URL']
        engine = create_engine(DATABASE_URL)
        print('engine created')

        # load data
        selectQuery = 'select * from lyrics_table'
        lyrics_df = pd.read_sql(selectQuery, engine)

        # train model
        genre_names = lyrics_df.groupby('genre').size().index.tolist()
	    
        X = lyrics_df['lyrics']
        Y = lyrics_df['genre']
	    
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
	    
        cv = Tokenizer(n_jobs = 4,
                       cv = 3,
                       verbose = 5
        )
        cv.fit(X_train, Y_train)
	    
        Y_pred = cv.predict(X_test)
        print(classification_report(Y_test, Y_pred))

        # export model
        pickle_write = open(pickle_file, 'wb')
        pickle.dump(cv, pickle_write)
        print('Model saved to {}'.format(pickle_file))

    else:
        print('You have passed in {} arguments.'.format(len(sys.argv)))
        print('Please provide the name of the pickle file to save.\n'\
              'Example: python create_model.py data/classifier.pkl')

if __name__ == '__main__':
    main()