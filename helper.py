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
    
    # print("--------------------------------- helper")
    # print(volumeInfo)
    # print("---------------------------------helper")
    
    #funcionoo
    try :
        img =response["items"][0]["volumeInfo"]["imageLinks"]
        resp={
        "totalItems":1,
        "averageRating":volumeInfo["averageRating"],
        "ratingsCount": volumeInfo["ratingsCount"],
        "description":volumeInfo["description"],
        "title":volumeInfo["title"],
        "author":volumeInfo["authors"][0],
        "img": img["thumbnail"],
        "fecha":volumeInfo["publishedDate"],
        
    }
    #si no existe un dato de informacion la tomara por 0(cero)
    except: 
        resp={
        "totalItems":1,
        "averageRating":0,
        "ratingsCount": 0,
        "description":volumeInfo["description"],
        "title":volumeInfo["title"],
        "author":volumeInfo["authors"][0],
        "img":0,
        "fecha":volumeInfo["publishedDate"],
        
    }
    
    return resp



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

