from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Hello World - Duniya Kaisi hai?"}


@app.get("/about")
def about():
    return { "Message" : "I am trying to test another endpoint in fastapi"}