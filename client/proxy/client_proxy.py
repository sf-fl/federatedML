
from flask import Flask
import flask.json


app = Flask(__name__)
@app.route("/train", methods=['post'])
def start_train():
    