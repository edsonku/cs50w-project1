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
    
    volumeInfo= response["items"][0]["volumeInfo"]["averageRating"]
    img =response["items"][0]["volumeInfo"]["imageLinks"]
    print("---------------------------------")
    print(volumeInfo)
    
    resp={
        "totalItems":1,
        "averageRating":response["items"][0]["volumeInfo"]["averageRating"],
        "ratingsCount": volumeInfo["ratingsCount"],
        "img": img["thumbnail"]
    }
    return volumeInfo
    return resp

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

