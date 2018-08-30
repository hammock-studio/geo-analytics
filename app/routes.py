from app import app
from flask import jsonify
from services.stream import tweets

@app.route('/')
@app.route('/index')
def index():
    return jsonify({ 'key': 'value'})

@app.route('/stream')
def stream():
    tweets()
