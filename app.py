import os
import string
import random
from flask import Flask,render_template,send_from_directory,request,redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tiny-url"
mongo = PyMongo(app)

def staticDir():
    return os.path.join(app.root_path, 'static')

def id_generator(size=8, chars=string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/favicon.png')
def favicon():
    return send_from_directory(staticDir(), 'favicon.png', mimetype='image/png')

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/shorten")
def shorten():
    url = request.args.get('url')
    if (not url):
        return 'Missing URL', 400
    
    slug=id_generator()
    mongo.db.url.insert({'url': url, 'slug': slug})

    return slug

@app.route("/<short_id>")
def view_data(short_id):
    doc = mongo.db.url.find_one_or_404({"slug": short_id})
    return redirect('http://'+doc['url'], code=302)
