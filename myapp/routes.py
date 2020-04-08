from myapp import app
import pandas as pd
import json, plotly
from flask import render_template, request
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from scripts.graphs import return_figures
from scripts.search_song import search_song
from scripts.myfunctions import remove_stop_words, tokenize
from scripts.song_results import get_song, apply_model

pickle_file = "./scripts/classifier.pkl"

@app.route('/')
@app.route('/index')
def jumbotron():
    return render_template('index.html')

@app.route('/')
@app.route('/capstone')
def capstone():
    return render_template('capstone.html')

@app.route('/capstone/eda')
def eda():
    """

    """
    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('eda.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/capstone/search')
def search_page():
    return render_template('search.html')

@app.route('/capstone/go')
def go():
    """Processes search item from user

    """
    # save user input in query
    query = request.args.get('query', '') 

    query_length = remove_stop_words(query)
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
    """
    """
    # save user input in query
    lyricId = request.args.get('lyricId', '')
    lyricCheckSum = request.args.get('lyricCheckSum', '')
    artist = request.args.get('artist', '')
    song = request.args.get('song', '')

    lyrics_text, clean_lyrics = get_song(lyricId, lyricCheckSum)
    classification_label = apply_model(pickle_file, clean_lyrics)

    lyrics_text = lyrics_text.split('\n')

    return render_template('results.html',
                           lyrics_text = lyrics_text,
                           classification_label = classification_label,
                           artist = artist,
                           song = song
    )