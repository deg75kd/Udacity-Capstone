from myapp import app
import sys

if len(sys.argv) == 2:
    run_location = sys.argv[1]

    if run_location == 'win':
        from waitress import serve
        serve(app, listen='*:8080')

    else:
        app.run(host='0.0.0.0', port=3001, debug=True)

else:
    app.run(host='0.0.0.0', port=3001, debug=True)