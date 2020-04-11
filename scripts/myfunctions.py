import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def tokenize(text):
    """Return clean tokens

    Args:
        text (string): block of text to tokenize

    Returns:
        clean_tokens (list): list of individual words
    """
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
        
    return clean_tokens

def remove_stop_words(query):
    """Get length of search string with stop words removed

    Args:
        query (string): name of searched for song

    Returns:
        (int): length of query with stop words removed
    """
    # create set of ChartLyrics API stop words
    stop_words = {'about', 'after', 'all', 'also', 'an', 'and', 'another', 
                  'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before',
                  'being', 'between', 'both', 'but', 'by', 'came', 'can', 
                  'come', 'could', 'did', 'do', 'does', 'each', 'else', 'for',
                  'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 
                  'here', 'him', 'himself', 'his', 'how', 'if', 'in', 'into', 
                  'is', 'it', 'its', 'just', 'like', 'make', 'many', 'me', 
                  'might', 'more', 'most', 'much', 'must', 'my', 'never', 'no',
                  'now', 'of', 'on', 'only', 'or', 'other', 'our', 'out',
                  'over', 're', 'said', 'same', 'see', 'should', 'since', 'so',
                  'some', 'still', 'such', 'take', 'than', 'that', 'the',
                  'their', 'them', 'then', 'there', 'these', 'they', 'this',
                  'those', 'through', 'to', 'too', 'under', 'up', 'use', 'very', 
                  'want', 'was', 'way', 'we', 'well', 'were', 'what', 'when', 
                  'where', 'which', 'while', 'who', 'will', 'with', 'would',
                  'you', 'your'}

    token_set = set(word_tokenize(query))
    search_set = token_set.difference(stop_words)

    return len(search_set)