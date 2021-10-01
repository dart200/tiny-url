import os
from flask import Flask, render_template,send_from_directory

app = Flask(__name__)

def staticDir():
    return os.path.join(app.root_path, 'static')

@app.route('/favicon.png')
def favicon():
    return send_from_directory(staticDir(), 'favicon.png', mimetype='image/png')

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/<short_id>")
def view_data(short_id):
    return "You are viewing short ID: {}".format(short_id)
