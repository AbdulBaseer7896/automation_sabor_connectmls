from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os



load_dotenv()  # load .env file

mongo = None

def init_db(app):
    global mongo
    print("this is the data base =  " , os.getenv("MONGO_URI"))
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo = PyMongo(app)
