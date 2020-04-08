import xml.etree.ElementTree as ET
import urllib
from urllib.request import urlopen
from sklearn.externals import joblib

from scripts.myfunctions import tokenize

# def tokenize(text):
    # tokens = word_tokenize(text)
    # lemmatizer = WordNetLemmatizer()
    
    # clean_tokens = []
    # for tok in tokens:
        # clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        # clean_tokens.append(clean_tok)
        
    # return clean_tokens

def get_song(lyric_id, lyric_check_sum):
    """
    """
    base_lyric_url = 'http://api.chartlyrics.com/apiv1.asmx/GetLyric?'
    qs_args = {
        'lyricId': lyric_id,
        'lyricCheckSum': lyric_check_sum
    }
    selected_url = base_lyric_url + urllib.parse.urlencode(qs_args)

    selected_response = urllib.request.urlopen(selected_url)
    selected_content = selected_response.read().decode('ascii')
    selected = ET.fromstring(selected_content)

    selected_lyrics = selected.find('{http://api.chartlyrics.com/}Lyric').text
    clean_lyrics = selected_lyrics.replace('\n', ' ')

    return selected_lyrics, clean_lyrics

def apply_model(pickle_file, text):
   """
   """
   model = joblib.load(pickle_file)
   classification_label = model.predict([text])[0]

   return classification_label