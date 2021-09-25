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

    #por si no tiene imagen
    try:
        img =response["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    except:
        img=0
    #por sino tiene puntuacion
    try:
        averageRating=volumeInfo["averageRating"]
        ratingsCount=volumeInfo["ratingsCount"]
    except:
        averageRating=0
        ratingsCount=0

    resp={
        "totalItems":1,
        "averageRating":averageRating,
        "ratingsCount": ratingsCount,
        "description":volumeInfo["description"],
        "title":volumeInfo["title"],
        "author":volumeInfo["authors"][0],
        "img": img,
        "fecha":volumeInfo["publishedDate"],
        "isbn":volumeInfo["industryIdentifiers"][0]["identifier"]  
    }
    
    return resp



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

