from myapp import app
import pandas as pd
import json, plotly
from flask import render_template, request
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

    """watch for stop words - make sure all words not eliminated
    about, after, all, also, an, and, another, any, are, as, at, be, because, been, before, being, between, both, but, by, came, can, come, could, did, do, does, each, else, for, from, get, got, had, has, have, he, her, here, him, himself, his, how, if, in, into, is, it, its, just, like, make, many, me, might, more, most, much, must, my, never, no, now, of, on, only, or, other, our, out, over, re, said, same, see, should, since, so, some, still, such, take, than, that, the, their, them, then, there, these, they, this, those, through, to, too, under, up, use, very, want, was, way, we, well, were, what, when, where, which, while, who, will, with, would, you, your

    """

    # get results
    results_df = search_song(query)

    # This will render the go.html
    return render_template('go.html', 
                           query = query, 
                           table = results_df
    )