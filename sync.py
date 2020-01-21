from flask import Flask, escape, request
from conf import Config

app = Flask(__name__)

def get_labels():
    pass

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'