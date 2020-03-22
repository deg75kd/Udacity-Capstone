from myapp import app
import json, plotly
from flask import render_template
# from wrangling_scripts.wrangle_data_project import return_figures

@app.route('/')
@app.route('/index')
def index():
    return 'Index Page'