from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__,
            template_folder="./",
            static_folder="./static")
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ =='__main__':
    import sys
    os.chdir((sys.path[0]))
    app.run(host='0.0.0.0',port='8082')
