
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet():
    return "Hey, Backend Developer"


greet()