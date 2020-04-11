# Udacity DSND - Song Lyrics Genre Predictor

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

* ChartLyrics API.ipynb
* Genius API.ipynb
* Lyrics EDA.ipynb
* Lyrics Graphs.ipynb
* Lyrics ML.ipynb
* Lyrics Model.ipynb
* myapp.py
* myapp-win.py
* nltk.txt
* Procfile
* requirements.txt

* data/classifier.pkl
* data/cls_report.pkl
* data/cnf_df.pkl
* data/lyrics.csv

* myapp/__init__.py - Runs the web application
* myapp/routes.py - 
* myapp/templates/go.html - Web page called when a search is executed
* myapp/templates/master.html - Home web page; also performs some data analysis
* models/classifier.pkl - Pickle file; output of train_classifier.py
* models/train_classifier.py - Trains and tests classification model

## Prerequisites

Flask 0.12.4\
gunicorn 19.9.0\
itsdangerous 0.24\
Jinja2 2.10\
json\
nltk 3.2.5\
numpy 1.12.1\
pandas 0.23.3\
pickle 0.7.4\
plotly 2.0.15\
python 3.6\
scikit-learn 0.19.1\
SQLAlchemy 1.2.18\
SQLite3\

## Running the Code

First, you have to execute the ETL pipeline that cleans data and stores it in a SQLite database.
```
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```

Next, you have to run the machine learning pipeline that trains the classifier and saves it as a pickle file.
```
python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl
```

Finally, to start the web application, run this.
```
python run.py
```

## Results

Over half of the messages are catgorized as "related", while just shy of half fall into the genre of news.  With the categories, each message can be classified into multiple categories.  If we then look at the number of categories each message falls into, there is an almost logarithmic decline.  Most messages don't fit into any category, and very few fit into more than ten.  There is a massive drop-off at two categories.  Based on the rest of the graph, this might deserve more investigation.

As for the classification model, testing reveals the average f1-score of most categories to be at 0.9 or higher.

## Built With

* [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/#starter-template) - The web framework used
* [Plotly](https://cdn.plot.ly/plotly-latest.min.js) - API for generating graphs

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
