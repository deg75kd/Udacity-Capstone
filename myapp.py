import sys
from myapp import app

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
        
    return clean_tokens

if len(sys.argv) == 2:
    run_location = sys.argv[1]

    if run_location == 'win':
        from waitress import serve
        serve(app, listen='*:8080')

    else:
        app.run(host='0.0.0.0', port=3001, debug=True)

else:
    app.run(host='0.0.0.0', port=3001, debug=True)