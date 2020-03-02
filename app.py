from flask import Flask, render_template, jsonify, redirect
import pymongo
import mars_scrape
from pprint import pprint

app = Flask(__name__)

CONN = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONN)
db = client.mars_db
collection = db.mars_data

@app.route("/scrape")
def scrape():
    mars = mars_scrape.scrape()
    db.mars_data.insert_one(mars)
    return redirect("http://localhost:5000/", code=302)

@app.route("/")
def index():
    mars_info = db.mars_data.find_one()
    return render_template ("index.html", mars_info=mars_info)

# results_from_db = list(db.results.find())
# pprint(results_from_db)


if __name__ == "__main__":
    app.run(debug=True)
