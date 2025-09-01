# Importing fastapi and json
from fastapi import FastAPI
import json

# loading data patient.json
# Function is opening a json file to read the data
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

# Creating an instance of FastAPI class
app = FastAPI()

# Decorator to tell about the path
@app.get("/")
def hello():
    return { "message": "Patient Management System API" }

@app.get("/about")
def about():
    return { "messages" : "You are in about section broooo - This is fully functional API to manage patient records" }


@app.get("/view")
def view():
    data = load_data() # calling the function load_data
    return data