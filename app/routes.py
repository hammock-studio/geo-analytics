from app import app
from flask import jsonify
from services.stream import tweets
from services.create import create

@app.route('/')
@app.route('/index')
def index():
    return jsonify({ 'key': 'value'})

@app.route('/stream')
def stream():
    tweets()

@app.route('/create')
def create():
    return jsonify({'loc': 'create'})
