from flask import Flask

app = Flask(__name__)

from myapp import routes
from scripts.myfunctions import tokenize
# def tokenize(text):
    # tokens = word_tokenize(text)
    # lemmatizer = WordNetLemmatizer()
    
    # clean_tokens = []
    # for tok in tokens:
        # clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        # clean_tokens.append(clean_tok)
        
    # return clean_tokens