from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scrape_mars import mars_scrape


app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars_html=mars)

@app.route('/scrape_mars')
def scrape():
    mars = mongo.db.mars
    mars_data = mars_scrape()

    mars.update({}, mars_data, upsert=True)
    return redirect('/')


if __name__=="__main__": 
    app.run(debug=True)
