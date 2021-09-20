import os
from functools import wraps
from re import search
from weakref import ProxyTypes
from flask import Flask, render_template, request, session, url_for, flash, redirect
from flask.helpers import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helper import apigoogle, login_required
#from googletrans import Traslator 
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

@app.route("/",methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        #ingreso y busqueda del libro por medio de isbn,author o titulo del libro
        busqueda= request.form.get("busqueda")
        print("success--------------")
        busqueda=db.execute("SELECT * FROM library WHERE isbn =:isbn OR title=:title OR author=:author",{"isbn":busqueda, "title":busqueda, "author":busqueda}).fetchall()
        
        #si no hay resultado debera enviar un mensaje
        if not busqueda:
            flash("no esta ese libro ¯\_(ツ)_/¯")
            print("cero")
            redirect("/")
        search=busqueda

        return render_template('index.html',search=search)

    else:
        return render_template("index.html")
        # libro_existente = db.execute("SELECT title,author FROM library WHERE ").fetchall()
        # comentario=reseñas
        # print(comentario)

    
    
    #  print(libro_existente)


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
        
        busqueda_user = db.execute("SELECT * FROM usuarios WHERE nombre = :username",
                            {"username":nombre}).fetchall()

        if not busqueda_user:
            flash('usurio no registrado')
            return redirect(url_for("login"))
        print(busqueda_user)
        if len(busqueda_user) != 1 or not check_password_hash(busqueda_user[0]["contraseña"], request.form.get("password")):
            print("invalida contraseña")
            flash('invalida')
            return render_template("login.html")

        session["user_id"] = busqueda_user[0]["id_usuario"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("/login.html")

# def reseñas():
    
#         user_id = session["user_id"]
#         comentario =request.form.get("comentario")
#         print("----------------------------.comentario")
#         print(comentario)
#         print(user_id)
#         #reseñas=db.execute("INSERT INTO reseñas (id_libro, id_usuario, comentario, valoracion)\ VALUES (:id_libro, id_usuario, reseña, valoracion)",{"id_libro":nombre, "id_usuario":user_id, "reseña":  ,"valoracion": })
#         #print("registrado")
#         #db.commit() 
#         return comentario
    

@app.route("/library/<string:isbn>", methods=["GET", "POST"])
def libro(isbn):
    if request.method == "POST":
        user_id = session["user_id"]
        comentario =request.form.get("comentario")
        print("----------------------------.comentario")
        # print(comentario)
        # print(user_id)
        #traer el id_libro
        id_libro=db.execute("SELECT * FROM library WHERE isbn=:isbn", {"isbn":isbn}).fetchall()
        print(id_libro[0]["id_libro"])
        id_libro=id_libro[0]["id_libro"]

        #reseñas=db.execute("INSERT INTO reseñas (id_libro, id_usuario, comentario, valoracion)\ VALUES (:id_libro, :id_usuario, :reseña, :valoracion)",{"id_libro":nombre, "id_usuario":user_id, "reseña":comentario,"valoracion":valoracion})
        #print("reseñas")
        #db.commit() 
        return redirect(url_for("index"))

    else:
        info = apigoogle(isbn)
        # si no existe el libro en la base de datos mandara un error
        if info["totalItems"] == 0:
            flash("Libro inexistente")
            return render_template("error.html"),404

        #traigo la imagen de la biblioteca para enviarsela al html
        portada=info["img"]

        return render_template("libro.html",info=info,portada=portada, isbn=isbn)

@app.route("/library")
def library():
    #muestras los libros que estan en la base de datos
    libro_existente=db.execute("SELECT * FROM library LIMIT 10").fetchall()
    print(libro_existente)
    libro_existente=libro_existente
    return render_template("library.html",libro_existente=libro_existente)

@app.route("/api/<string:isbn>")
def api(isbn):
    print(isbn)
    busqueda=db.execute("SELECT * FROM library WHERE isbn =:isbn",{"isbn":isbn}).fetchall()
    print(busqueda)
    #resultado de la api
    resapi={
        "isbn":busqueda[0]["isbn"],
        "author":busqueda[0]["author"],
        "title":busqueda[0]["title"],
        "year":busqueda[0]["year"]

    }
    return resapi