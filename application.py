import os

from flask import Flask, render_template, request, session, url_for, flash
from flask.helpers import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registro",methods=["GET", "POST"])
def registro():
    if request.method == "POST":

        nombre = request.form.get("username")
        contraseña = generate_password_hash(request.form.get("password"))
        confirmacion = request.form.get("confirmation")
        if not request.form.get("username"):
            print("Obligatorio poner usuario")
            return render_template("registro.html")

        elif not request.form.get("password"):
            print("obligatorio poner contraseña")
            return render_template("registro.html")

        elif request.form.get("password") != confirmacion:
            print("las contraseñas deben ser las mismas")
            return render_template("registro.html")
        
        usuario_existente = db.execute("SELECT nombre from usuarios where nombre =:username", {"username": nombre})
        #print(usuario_existente)
        if  not usuario_existente:
            print("intenta otro nombre")
            flash(u'Invalid password provided', 'error')
            return render_template("registro.html")
        else:
            usuario_nuevo = db.execute("INSERT INTO usuarios (nombre, contraseña) \
                                       VALUES (:username, :password)",{"username":nombre, "password":contraseña})
            
            #session["usuarios_id"] = usuario_nuevo[0]["id"]
            # print(session["usuarios_id"])
            print("registrado")
            db.commit() 
                            
            return render_template("index.html")
    else:
        return render_template("registro.html")

@app.route("/login.html",methods=["GET","POST"])
def login():
    session.clear()
    nombre = request.form.get("username")
    contraseña = generate_password_hash(request.form.get("password"))
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template ("login.html")

        elif not request.form.get("password"):
            return render_template ("login.html")

        busqueda = db.execute("SELECT * FROM users WHERE usuarios = :username",
                          {"username":nombre})

        if len(busqueda) != 1 or not check_password_hash(busqueda[0]["contraseña"], request.form.get("password")):
            print("invalida contraseña")
            return render_template ("login.html")

        session["usuarios_id"] = busqueda[0]["id"]

        return render_template("index.html")
    else:
        return render_template ("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("/")
