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
# def tokenize(text):
    # tokens = word_tokenize(text)
    # lemmatizer = WordNetLemmatizer()
    
    # clean_tokens = []
    # for tok in tokens:
        # clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        # clean_tokens.append(clean_tok)
        
    # return clean_tokens

def main():
    """
    """
    if len(sys.argv) == 4:
        model_file, cnf_matrix_file, cls_report_file = sys.argv[1:]
    
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
        # X = lyrics_df['lyrics'].apply(tokenize)
        Y = lyrics_df['genre']
	    
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
	    
        # pipeline = Pipeline([
            # ('vect', CountVectorizer(tokenizer = tokenize)),
            # ('tfidf', TfidfTransformer()),
            # ('clf', RandomForestClassifier())
        # ])
        pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer = None, stop_words='english')),
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
	    
        # export model
        model_pkl = open(model_file, 'wb')
        pickle.dump(cv, model_pkl)
        model_pkl.close()
        print('Model saved to {}'.format(model_file))

        # save confusion matrix
        Y_pred = cv.predict(X_test)
        cnf_matrix = confusion_matrix(Y_test, Y_pred)
        cnf_matrix_df = pd.DataFrame(data = cnf_matrix,
                                     index = genre_names,
                                     columns = genre_names)
        cnf_matrix_pkl = open(cnf_matrix_file, 'wb')
        pickle.dump(cnf_matrix, cnf_matrix_pkl)
        cnf_matrix_pkl.close()
        print('\nConfusion matrix saved to {}'.format(cnf_matrix_file))
        
        # save classification report
        cls_report = classification_report(Y_test, Y_pred)
        cls_report_pkl = open(cls_report_file, 'wb')
        pickle.dump(cls_report, cls_report_pkl)
        cls_report_pkl.close()
        print('\nConfusion matrix saved to {}'.format(cls_report_file))

    else:
        print('You have passed in {} arguments.'.format(len(sys.argv)))
        # print('Please provide the name of the pickle file to save.\n'\
              # 'Example: python create_model.py data/classifier.pkl')
        print('Please provide the name of the pickle files to save.\n'\
              'Example: python create_model.py data/classifier.pkl data/cnf_df.pkl data/cls_report.pkl')


if __name__ == '__main__':
    main()