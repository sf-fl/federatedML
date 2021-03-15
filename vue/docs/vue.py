from flask import Flask, render_template
import os

app = Flask(__name__,
            template_folder="./",
            static_folder="./static")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ =='__main__':
    import sys
    os.chdir((sys.path[0]))
    app.run(host='localhost',port='8082')
