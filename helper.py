import requests 
from functools import wraps
from flask import session,  redirect
def apigoogle(isbn):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn).json()

    total_item= response["totalItems"]

    if not total_item:
        resp ={
            "totalItems":0
        }
        return resp
    
    volumeInfo= response["items"][0]["volumeInfo"]
    img =response["items"][0]["volumeInfo"]["imageLinks"]
    print("--------------------------------- helper")
    print(volumeInfo)
    print("---------------------------------helper")
    print(volumeInfo["ratingsCount"])
    print("---------------------------------helper")
    resp={
        "totalItems":1,
        "averageRating":volumeInfo["averageRating"],
        "ratingsCount": volumeInfo["ratingsCount"],
        "description":volumeInfo["description"],
        "title":volumeInfo["title"],
        "author":volumeInfo["authors"],
        "img": img["thumbnail"]
    }
    
    return resp

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

