from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template (display data) from Mongo database 
@app.route("/")
def home():

    # Find one record of data from the mongo database
    Mars_Info = mongo.db.mars.find_one() 
    print(Mars_Info)

    # Return template and data
    return render_template("index.html", data=Mars_Info)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    #Run Scrape function, scrape()
    Mars_Data = scrape_mars.scrape()
    
    # Update the Mongo database
    mongo.db.mars.update({},Mars_Data,upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

