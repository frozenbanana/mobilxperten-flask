from mobilXpertenApp import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/sallad')
def sallad():
    return "Hello, Sallad!"