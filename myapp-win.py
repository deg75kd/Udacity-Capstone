from myapp import app
#app.run(host='0.0.0.0', port=3001, debug=True)

from waitress import serve
serve(app, listen='*:8080')