# Udacity DSND - Song Lyrics Genre Predictor

[Web Page](https://kdj-portfolio.herokuapp.com/capstone)

## Table of Contents

* [Summary](#summary)
* [File Descriptions](#file-descriptions)
* [Prerequisites](#prerequisites)
* [Running the Code](#running-the-code)
* [Results](#results)
* [Built With](#built-with)
* [License](#license)

## Summary

This project presents my efforts to categorize song lyrics using Data Science.  The first step was to obtain a dataset of song lyrics.  After looking at several options, I decided on a dataset hosted on kaggle.com by the user gyani95.  It is a large dataset with several genres represented.  The next step in the process was to clean the data.  I found it to be pretty messy and required a fair amount of clean up.  After I had the data in a suitable state, I analyzed it so identify some of the more interesting trends in this particular dataset.  From that analysis I created a number of graphics to illustrate my findings.  Then I created a machine learning pipeline and fed in the dataset to create a predictive model.  I also captured the results of the model so users can see how accurate it is.  Finally, I created a process that allows a user to search for a song and apply the machine learning model to it.  This results in the predicted genre of the song.

## File Descriptions

* ChartLyrics API.ipynb - Using ChartLyrics API
* Genius API.ipynb - Using Genius API
* Lyrics EDA.ipynb - Exploratory data analysis
* Lyrics Graphs.ipynb - Creating EDA graphs
* Lyrics ML.ipynb - Creating the machine learning model
* Lyrics Model.ipynb - Viewing results of the ML model
* myapp.py - Runs the web page server
* nltk.txt - Installs NLTK punkt package on Heroku
* Procfile - Indicates use of gunicorn on Heroku
* requirements.txt - Package requirements to be installed on Heroku

* data/classifier.pkl - Machine learning model
* data/classifier_sm.pkl - Machine learning model using 10,000 rows (due to memory constraints)
* data/cls_report.pkl - Classification report
* data/cnf_df.pkl - Confusion matrix
* data/lyrics.csv - CSV with original data

* myapp/__init__.py - Runs the Flask web application
* myapp/routes.py - Renders the web pages
* myapp/static/* - CSS, JavaScript and image files for the Bootstrap template
* myapp/templates/capstone.html - Home web page for the capstone project
* myapp/templates/eda.html - Web page discussing exploratory data analysis
* myapp/templates/go.html - Web page called when a search is executed
* myapp/templates/mldata.html - Web page discussing the machine learning model
* myapp/templates/results.html - Web page that displays the results of the user search
* myapp/templates/search.html - Web page that allows user to search for a song

* scripts/create_model.py - Creates the machine learning model
* scripts/graphs.py - Creates the EDA graphs
* scripts/ml_graphs.py - Creates the machine learning graph
* scripts/myfunctions.py - Functions called from other scripts
* scripts/process_data.py - Pulls data from the CSV, cleans it and saves to a PostgreSQL database
* scripts/search_song.py - Performs user search for a song
* scripts/song_results.py - Applys the ML model to the search

* myapp/templates/Chicago Restaurant Recommender System.html - HTML export of a Jupyter notebook
* myapp/templates/Recommendations_with_IBM.html - HTML export of a Jupyter notebook

## Prerequisites

Flask 1.1.1\
gunicorn 20.0.4\
itsdangerous 1.1.0\
Jinja2 2.10\
joblib 0.14.1\
json\
MarkupSafe 1.1.1\
nltk 3.4.5\
numpy 1.18.1\
pandas 0.25.3\
pickle 0.7.5\
plotly 2.7.0\
psycopg2 2.8.4\
python 3.6\
requests 2.22.0\
scikit-learn 0.22.1\
SQLAlchemy 1.3.12\
urllib3 1.25.7\
Werkzeug 0.16.0\

## Running the Code

First you need to set the connection string for the PostgreSQL database that is hosted on Heroku. This is specific to each database.
```
set DATABASE_URL=postgres://...
```

Then you have to execute the ETL pipeline that cleans data and stores it in a PostgreSQL database on Heroku.  This takes 2 parameters:
1) The location of the CSV file
2) "hobby" to limit the output to 10,000 rows, or "live" to load the entire dataset
```
python scripts\process_data.py data\lyrics.csv [hobby | live]
```

Next, you have to run the machine learning pipeline that trains the classifier and saves it as a pickle file.  This accepts 3 parameters for the location of the pickle files to save.
```
python scripts/create_model.py data/classifier.pkl data/cnf_df.pkl data/cls_report.pkl
```

Finally, to start the web application, run this.
```
python myapp.py win
```
On a Windows system waitress is required. Then add a parameter to the command.
```
python myapp.py win
```

## Results

Due to the skew of the dataset the vast majority of tests are predicted to be in the Rock genre.  Thus, the overall accuracy is not that good.  Hip-Hop and Rock are the only genres where the F1-score is above 0.5.  However, due to the huge number of Rock songs in the dataset the overall accuracy is also just over 0.5.  I suspect applying this to real world data, where the Rock genre is not as heavily represented, would produce less promising results.

## Built With

* [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/#starter-template) - CSS framework
* [Plotly](https://cdn.plot.ly/plotly-latest.min.js) - API for generating graphs
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python-based Web framework
* [Heroku]() - Web hosting service
* [ChartLyrics]() - API for getting song lyrics

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
