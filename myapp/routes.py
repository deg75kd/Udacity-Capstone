from myapp import app
import pandas as pd
import json, plotly
from flask import render_template
from scripts.graphs import return_figures
from scripts.search_song import search_song

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

    # get results
    results_df = search_song(query)

    # This will render the go.html
    return render_template('go.html',tables=[results_df.to_html])