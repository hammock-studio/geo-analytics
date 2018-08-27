from app import app
from flask import jsonify
from services import searchfunc

@app.route('/')
@app.route('/index')
def index():
    return jsonify({ 'key': 'value'})


@app.route('/search')
def search():
    return searchfunc("Tal")
