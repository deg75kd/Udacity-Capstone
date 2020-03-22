import json
# import plotly
import pandas as pd

from flask import Flask
from flask import render_template, request, jsonify
# from plotly.graph_objs import Bar, Pie, Scatter

import process_data

app = Flask(__name__)

def main():
    """Runs web application"""

    # process data
    process_data.main()

if __name__ == '__main__':
    main()