import os
from functools import wraps
from flask import Flask, render_template, request, session, url_for, flash, redirect
from flask.helpers import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helper import apigoogle, login_required
#from datatime 

app = Flask(__name__)

# Check for environment variable
if not ("postgresql://kzpvqapggnigwp:fb9ae8eeee9d58ac9fa2ec10ad9f9ff7587a0505dc26de048128c2aee5de47fa@ec2-54-159-35-35.compute-1.amazonaws.com:5432/dfk5gp8sokvmov"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(
    "postgresql://kzpvqapggnigwp:fb9ae8eeee9d58ac9fa2ec10ad9f9ff7587a0505dc26de048128c2aee5de47fa@ec2-54-159-35-35.compute-1.amazonaws.com:5432/dfk5gp8sokvmov")
db = scoped_session(sessionmaker(bind=engine))



@app.errorhandler(404)
def page_no_found(e):
    return render_template("error.html"),404

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/registro",methods=["GET", "POST"])
def registro():
    if request.method == "POST":

        nombre = request.form.get("username")
        print(nombre)
        contraseña = generate_password_hash(request.form.get("password"))
        confirmacion = request.form.get("confirmation")
        if not request.form.get("username"):
            print("Obligatorio poner usuario")
            return redirect("registro.html")

        elif not request.form.get("password"):
            print("obligatorio poner contraseña")
            return redirect("registro.html")

        elif request.form.get("password") != confirmacion:
            print("las contraseñas deben ser las mismas")
            return render_template("registro.html")
        
        usuario_existente = db.execute("SELECT * from usuarios where nombre =:username", {"username": nombre}).fetchall()
        #print(usuario_existente)
        print(usuario_existente)
        
        if not usuario_existente:
            print("entro 2")
            usuario_nuevo = db.execute("INSERT INTO usuarios (nombre, contraseña) \
                                       VALUES (:username, :password)",{"username":nombre, "password":contraseña})
            print("registrado")
            session["user_id"] = usuario_nuevo[0]["id_usuario"]
            db.commit() 
            return redirect(url_for("index"))
        
        else:
            print("intenta otro nombre")
            flash(u'Intenta otro nombre')
            return render_template("registro.html")
    
    else:
        return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        
        if not request.form.get("username"):
            return render_template ("login.html")

        elif not request.form.get("password"):
            return render_template ("login.html")

        nombre = request.form.get("username")
        contraseña = generate_password_hash(request.form.get("password"))
        print(nombre,contraseña)
        
        busqueda = db.execute("SELECT * FROM usuarios WHERE nombre = :username",
                            {"username":nombre}).fetchall()

        if not busqueda:
            flash('usurio no registrado')
            return redirect(url_for("login"))
        print(busqueda)
        if len(busqueda) != 1 or not check_password_hash(busqueda[0]["contraseña"], request.form.get("password")):
            print("invalida contraseña")
            flash('invalida')
            return render_template("login.html")
        session["user_id"] = busqueda[0]["id_usuario"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("/login.html")

def reseñas():
    user_id = session["user_id"]
    comentario =request.form.get("comentario")
    print(comentario)
    #reseñas=db.execute("INSERT INTO reseñas (id_libro, id_usuario, comentario, valoracion)\ VALUES (:id_libro, id_usuario, reseña, valoracion)",{"id_libro":nombre, "id_usuario":user_id, "reseña":  ,"valoracion": })
    #print("registrado")
    #db.commit() 

@app.route("/book/<string:isbn>")
def libro(isbn):
    info = apigoogle(isbn)

    if info["totalItems"] == 0:
        return "No"


    return info

@app.route("/book")
def book():
    return render_template("book.html")
