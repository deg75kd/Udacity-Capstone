from myapp import app
import pandas as pd
import json, plotly
from flask import render_template, request
from scripts.graphs import return_figures
from scripts.search_song import search_song
from data.myfunctions import remove_stop_words

@app.route('/')
@app.route('/index')
def jumbotron():
    return render_template('index.html')

@app.route('/eda')
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

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/go')
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

@app.route('/results')
def results_page():
    """
    """
    # save user input in query
    lyricId = request.args.get('lyricId', '')
    lyricCheckSum = request.args.get('lyricCheckSum', '')

    return render_template('results.html',
                           lyricId = lyricId,
                           lyricCheckSum = lyricCheckSum
    )