import os
import pandas as pd
import plotly.graph_objs as go

import psycopg2
import sqlalchemy
from sqlalchemy import create_engine

def loaddata():
    """Loads data from database for analysis

    Args:
        None

    Returns:
        df (dataframe): data from database stored in a dataframe
    """
    DATABASE_URL = os.environ['DATABASE_URL']
    engine = create_engine(DATABASE_URL)
    
    selectQuery = "select * from lyrics_table"
    df = pd.read_sql(selectQuery, engine)
    
    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations
    """
    # load data
    lyrics_df = loaddata()

    # Bar chart of top 10 artists by song count
    graph_one = []
    df_top_artists = lyrics_df.groupby('artist').size().sort_values(ascending=False).reset_index(name='songs').head(10)

    graph_one.append(
        go.Bar(
            x = df_top_artists['artist'],
            y = df_top_artists['songs'],
            text = df_top_artists['songs'],
            textposition = 'auto'
        )
    )

    layout_one = dict(
        title = 'Top 10 Artists by Song Count',
        xaxis = dict(title = 'Artist'),
        yaxis = dict(title = 'Songs')
    )

    # Pie chart of song genres
    graph_two = []
    df_genre_count = lyrics_df.groupby('genre').size().sort_values(ascending=False).reset_index(name='songs')
    
    graph_two.append(
        go.Pie(
            labels = df_genre_count['genre'],
            values = df_genre_count['songs']
        )
    )
    layout_two = dict(title = 'Song Counts by Genre')

    # Line graph of song counts by year
    graph_three = []
    df_year_count = lyrics_df.groupby('year').size().reset_index(name='songs')
    
    graph_three.append(
        go.Scatter(
            x = df_year_count['year'],
            y = df_year_count['songs'],
            mode = 'lines+markers',
            name = 'Songs by Year'
        )
    )
    layout_three = dict(
        title = 'Songs by Year',
        xaxis = dict(title = 'Year'),
        yaxis = dict(title = 'Songs')
    )

    # Boxplots of lyric lengths by genre
    graph_four = []
    genre_list = lyrics_df.groupby('genre').size().index.tolist()
    
    for genre in genre_list:
        length_list = lyrics_df[lyrics_df['genre'] == genre]['lyrics-length'].values.tolist()
        graph_four.append(
            go.Box(
                y = length_list,
                name = genre
            )
        )
    layout_four = dict(title = 'Lyric Lengths by Genre')

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures