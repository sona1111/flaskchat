from views import app, fl

def ghz():
    app.run(fl, port = 4448, host = '0.0.0.0')
