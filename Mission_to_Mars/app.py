from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Setup mongo connection
conn = "mongodb://localhost:27017/mars_db"
client = pymongo.MongoClient(conn)


@app.route("/")
def index():
    mars_data = client.db.mars.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars = client.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    print(mars_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
