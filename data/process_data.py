import os
import sys
import subprocess
import pandas as pd
import re
import io

import psycopg2
from sqlalchemy import create_engine

def clean_data(df_lyrics):
    """Separates categories in dataframe into different columns.
    
    Args:
        df_lyrics: Dataframe with music lyrics
    
    Returns:
        Dataframe that is ready for analysis and modeling
    """

    # drop null data
    df_lyrics = df_lyrics.dropna(axis=0)
    # remove newline characters
    df_lyrics['lyrics'] = df_lyrics.apply(lambda x: x['lyrics'].replace('\n',' '), axis=1)

    # remove lyrics below threshold
    df_lyrics['lyrics'] = df_lyrics['lyrics'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]', ' ', x))
    df_lyrics['lyrics-length'] = df_lyrics['lyrics'].apply(lambda x: len(x) - x.count(' '))
    df_lyrics = df_lyrics[df_lyrics['lyrics-length'] > 100]

    # remove lyrics that failed to load
    df_lyrics = df_lyrics[~df_lyrics['lyrics'].str.contains('We are not in a position to display')]

    # remove remixes
    df_lyrics = df_lyrics[~df_lyrics['song'].str.contains('remix', flags=re.IGNORECASE, regex=True)]

    # fix years
    df_lyrics.at[27657, 'artist'] = '702'
    df_lyrics.at[27657, 'year'] = 2003
    df_lyrics.at[315540, 'artist'] = 67
    df_lyrics.at[315540, 'year'] = 2016
    df_lyrics.at[335205, 'year'] = 2001

    # remove top lyrics with lots of duplicates
    df_lyrics = df_lyrics[~df_lyrics['lyrics'].str.contains('feat  Philip Lawrence   Her Heart Is Racing')]

    return df_lyrics

def save_data(df_lyrics, run_mode):
    """Saves dataframe to a PostgreSQL database.
    
    Args:
        df_lyrics: Dataframe to be saved
        run_mode: hobby = load only 10,000 rows
                  live = load entire dataframe
    """

    # DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a kd-capstone')

    # proc = subprocess.Popen('heroku',
                            # 'config:get',
                            # 'DATABASE_URL',
                            # '-a',
                            # 'kd-capstone', 
                            # stdout=subprocess.PIPE)
    # DATABASE_URL = proc.stdout.read()
    DATABASE_URL ='postgres://ibgwytquyfcsae:a69a7fcd93593ab2cfa8de1a1d29500755d48ec728912be681801bb2b101cb2a@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dk3ib67dg3lj4'

    # print(DATABASE_URL)
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    engine = create_engine(DATABASE_URL)

    # df_lyrics.to_sql('lyrics_table', conn, if_exists='replace', index=False)
    # create empty table, or truncate existing table
    df_lyrics.head(0).to_sql('lyrics_table', engine, if_exists='replace', index=False)

    # load table by row
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    if run_mode == 'live':
        df_lyrics.to_csv(output, sep='\t', header=False, index=False)
    else:
        df_lyrics.head(10000).to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'lyrics_table', null="")
    conn.commit()

    return None

def main():
    """Performs ETL from CSV files to a PostgreSQL database.
    
    Args (command-line):
        data_filepath: CSV file of lyrics
        run_mode: determines if whole dataframe or part loaded to DB
    """

    if len(sys.argv) == 3:

        data_filepath, run_mode = sys.argv[1:]

        print('Loading data from {}...'.format(data_filepath))
        df_lyrics = pd.read_csv(data_filepath, index_col='index')

        print('Cleaning data...')
        df_lyrics = clean_data(df_lyrics)

        print('Saving data...')
        try:
            save_data(df_lyrics, run_mode)
            print('Cleaned data saved to database!')
        except:
            print('ERROR: Data was not saved to the database!')

    else:
        print('Please provide the filepaths of the lyrics dataset as the '\
              'first argument and either "hobby" or "live" for the second '\
              'argument. \n\nExample: python process_data.py lyrics.csv '\
              'hobby')


if __name__ == '__main__':
    main()