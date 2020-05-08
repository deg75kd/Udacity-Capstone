from myapp import app
import numpy as np
import pandas as pd
import json, plotly
import pickle
from flask import render_template, request
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.externals import joblib

from scripts.graphs import return_figures
from scripts.ml_graphs import return_ml_figures
from scripts.search_song import search_song
from scripts.myfunctions import remove_stop_words
from scripts.song_results import get_song, apply_model

# model_pkl = "./data/classifier.pkl"
model_pkl = "./data/classifier_sm.pkl"
cnf_matrix_pkl = "./data/cnf_df.pkl"
cls_report_pkl = "./data/cls_report.pkl"

@app.route('/')
@app.route('/index')
def jumbotron():
    """Render the main portfolio page

    Args:
        None

    Returns:
        index.html page
    """
    return render_template('index.html')

@app.route('/capstone')
def capstone():
    """Render the main page for the capstone project

    Args:
        None

    Returns:
        capstone.html page
    """
    return render_template('capstone.html')

@app.route('/capstone/eda')
def eda():
    """Render the page for exploratory data analysis

    Args:
        None

    Returns:
        eda.html page
    """
    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('eda.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/capstone/mldata')
def mldata():
    """Render the page for exploratory data analysis

    Args:
        None

    Returns:
        mldata.html page
    """
    # load classification report
    file = open(cls_report_pkl, 'rb')
    cls_report = pickle.load(file)
    file.close()

    # call script to generate graphs
    figures = return_ml_figures(cnf_matrix_pkl)

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('mldata.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                           cls_report = cls_report
    )

@app.route('/capstone/search')
def search_page():
    """Render the page to search for songs

    Args:
        None

    Returns:
        search.html page
    """
    return render_template('search.html')

@app.route('/capstone/go')
def go():
    """Processes search item from user

    Args:
        None

    Returns:
        go.html page
    """
    # save user input in query
    query = request.args.get('query', '') 

    query_length = remove_stop_words(query)
    # print('Query length: {}'.format(query_length))
    if query_length > 0:
        results_df = search_song(query)
	    
    else:
        query = 'All the words you entered are identified as stop words by ChartLyrics. The query cannot be executed.'
        results_df = pd.DataFrame(columns = ['lyric_id', 'lyric_check_sum', 'artist', 'song'])

    return render_template('go.html', 
                           query = query,
                           table = results_df
    )

@app.route('/capstone/results')
def results_page():
    """Render the page with the search results

    Args:
        None

    Returns:
        results.html page
    """
    # save user input in query
    lyricId = request.args.get('lyricId', '')
    lyricCheckSum = request.args.get('lyricCheckSum', '')
    artist = request.args.get('artist', '')
    song = request.args.get('song', '')

    lyrics_text, clean_lyrics = get_song(lyricId, lyricCheckSum)
    classification_label = apply_model(model_pkl, clean_lyrics)
    # classification_label = model.predict([clean_lyrics])[0]

    lyrics_text = lyrics_text.split('\n')

    return render_template('results.html',
                           lyrics_text = lyrics_text,
                           classification_label = classification_label,
                           artist = artist,
                           song = song
    )

@app.route('/recibm')
def recibm():
    """Render the page for recommendations with IBM

    Args:
        None

    Returns:
        Recommendations_with_IBM.html page
    """
    return render_template('Recommendations_with_IBM.html')

@app.route('/coursera')
def coursera():
    """Render the page for my Coursera capstone project

    Args:
        None

    Returns:
        Chicago Restaurant Recommender System.html page
    """
    return render_template('Chicago Restaurant Recommender System.html')