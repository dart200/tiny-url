import os
import string
import random
from flask import Flask,render_template,send_from_directory,request,redirect
from flask_pymongo import PyMongo

application = Flask(__name__)
mongo_login = None if not os.getenv('MONGODB_USERNAME') else os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@'
application.config["MONGO_URI"] = 'mongodb://' + (mongo_login if mongo_login else '') + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(application)

def staticDir():
    return os.path.join(application.root_path, 'static')

def id_generator(size=8, chars=string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@application.route('/favicon.png')
def favicon():
    return send_from_directory(staticDir(), 'favicon.png', mimetype='image/png')
@application.route('/main.js')
def mainjs():
    return send_from_directory(staticDir(), 'main.js')


@application.route("/")
@application.route("/index")
def index():
    return render_template('index.html')

@application.route("/shorten")
def shorten():
    url = request.args.get('url')
    if (not url):
        return 'Missing URL', 400

    while True:
        slug=id_generator()
        if (not mongo.db.url.find_one({'slug': slug})):
            mongo.db.url.insert({'url': url, 'slug': slug})
            return render_template('index.html', url=request.url_root+slug)


@application.route("/<short_id>")
def view_data(short_id):
    doc = mongo.db.url.find_one_or_404({"slug": short_id})
    return redirect('http://'+doc['url'], code=302)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.getenv("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.getenv("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)