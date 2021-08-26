import os

from flask import Flask, render_template, request, session, url_for
from flask_session import Session
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

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM usuarios WHERE Nombre = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
 
 @app.route("/registro", methods=["GET", "POST"])
 def registro:
     if request.method == "POST":
            # asegurar envio de usrname
        # Parte tomada del codigo usado en la clase 28
        if not request.form.get("username"):
            return apology("Ingrese un usuario", 400)

        # asegurar envio de pswd
        elif not request.form.get("password"):
            

        # verificar si contraseña es la misma
        elif request.form.get("password") != request.form.get("confirmation"):

        # Verifica si el usuario ya existe
        usuario_existente = db.execute("SELECT * from users where username =:username", username=request.form.get("username"))

        if usuario_existente:
           

        else:
            usuario_nuevo = db.execute("INSERT INTO users (username, hash) \
                                       VALUES (:username, :password)",
                                       username=request.form.get("username"), password=generate_password_hash(request.form.get("password")))

            session["user_id"] = usuario_nuevo
            flash("registrado")
            return render_template("index.html")

    else:
        return render_template("register.html")
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("/")

