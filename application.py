import os, json
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session 
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from wtform_fields import *
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session
import requests
import datetime
from datetime import datetime

app = Flask(__name__)

def before_request():
    app.jinja_env.cache = {}
    app.before_request(before_request)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


app.secret_key = 'replace later'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']=(os.getenv("DATABASE_URL"))
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)
engine = create_engine(os.getenv("DATABASE_URL"))
exe = scoped_session(sessionmaker(bind=engine))

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))  

@app.route("/")    
def index():
    """ Show search box """
        
    return render_template("index.html")

@app.route("/registration", methods=['GET', 'POST'])
def registration():


    reg_form = RegistrationForm()
        
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
            
        hashed_pass = pbkdf2_sha512.hash(password)
            
        user = User(username=username, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        flash('Registered successfully. Please Login', 'success')
        return redirect(url_for('login'))
            
    return render_template( "registration.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    username = request.form.get("username")
    login_form= LoginForm()
    
    if login_form.validate_on_submit():
        
        
        user_object = User.query.filter_by(username = login_form.username.data).first()
        login_user(user_object)
        session['username'] = username
        session.permanent = True
        return redirect(url_for('restrict'))
        
        
        return "User not logged in"
    
  

    return render_template("login.html", form=login_form)

@app.route("/restrict", methods=['GET', 'POST'])    
def restrict():
    """ Show search box """
    username = session["username"]
    
    if not current_user.is_authenticated:
        flash('Please login', 'you need to login first')
        return redirect(url_for('login'))
    
    lands=exe.execute("select g.landscape, COUNT(r1.comment)as comments,\
                COUNT(r1.rating) as ratings\
                from gallery g\
                JOIN reviews r1 on r1.idphoto=g.idphoto\
                GROUP By g.landscape\
                ORDER BY COUNT(r1.comment) DESC, \
                COUNT(r1.rating) DESC LIMIT 1;")
    landscape= lands.fetchall()
    
    calc = exe.execute("SELECT r.username, \
    COUNT(r.comment) as comments, \
    COUNT(r.rating) as rating FROM reviews r\
    GROUP by r.username \
    ORDER BY COUNT(r.comment) DESC, \
    COUNT(r.rating) DESC LIMIT 1")
    maxP = calc.fetchall()

    rUser = exe.execute("SELECT u.username \
                    FROM users u JOIN reviews r\
                    ON u.username= r.username\
                    ORDER BY timeDate DESC LIMIT 1")
    recent = rUser.fetchall()
    
    weath= exe.execute("select g.weather, COUNT(r1.comment) as comments,\
                    COUNT(r1.rating) as ratings\
                    from gallery g\
                    JOIN reviews r1 on r1.idphoto=g.idphoto\
                    GROUP By g.weather\
                    ORDER BY COUNT(r1.comment) DESC, \
                    COUNT(r1.rating) DESC LIMIT 1;")
    weather=weath.fetchall()
    
    return render_template("restrict.html", username=username, landscape=landscape, maxP=maxP, 
    recent=recent, weather=weather)

@app.route("/draws", methods=['GET'])
def draws():  
    
    username = session["username"]
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
        
    return render_template("draws.html", username=username)
    
@app.route("/results", methods=['GET'])
def results():

    username = session["username"]
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))

    
    if not request.args.get("image"):
        return render_template("error.html", message="you must provide a image.")

    query = "%" + request.args.get("image") + "%"

    #query = query.idphoto()#
    
    rows = exe.execute("SELECT idphoto, location, url, weather, landscape FROM gallery WHERE \
                        idphoto LIKE :query OR \
                        weather LIKE :query OR \
                        landscape LIKE :query OR \
                        location LIKE :query \
                        ORDER by location",
                        {"query": query})
    
    # gallery not founded
    if rows.rowcount == 0:
        return render_template("error.html", message="we can't find with that description.")
    
    # Fetch all the results
    gallery = rows.fetchall()
    
    
    
    return render_template("results.html", gallery=gallery, username=username)
    
@app.route("/logout", methods=['GET' ])
def loggedout():
    
    session.clear()
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
    
@app.route("/image/<idphoto>", methods=['GET','POST'])
def image(idphoto):
    
    
    username = session["username"]
    timeDate = datetime.now()
    #timeDate = now.strftime("%d/%m/%Y,' ',%H:%M:%S")
    
    if request.method == "POST":
        
        
        # Save current user info
        
        # Fetch form data
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        
        # Search idphoto by idphoto
        row = exe.execute("SELECT idphoto FROM gallery WHERE idphoto = :idphoto",
                        {"idphoto": idphoto})

        # Save id into variable
        bookId = row.fetchone() # (id,)
        bookId = bookId[0]

        # Check for user submission (ONLY 1 review/user allowed per book)
        row2 = exe.execute("SELECT * FROM reviews WHERE username = :username AND idphoto = :idphoto",
                    {"username": username,
                     "idphoto": idphoto})

        # A review already exists
        if row2.rowcount == 1:
            
            flash('You already submitted a review for this book', 'warning')
            return redirect("/image/" + idphoto)

        # Convert to save into DB
        rating = int(rating)

        exe.execute("INSERT INTO reviews (timeDate, username,  comment, idphoto, rating) VALUES \
                    (:timeDate, :username,  :comment, :idphoto, :rating)",
                    {"timeDate": timeDate,
                    "username": username, 
                    "comment": comment, 
                    "idphoto": idphoto, 
                    "rating": rating})

        # Commit transactions to DB and close the connection
        exe.commit()

        flash('Review submitted!', 'info')

        return redirect("/image/" + idphoto)
    
    # Take the book ISBN and redirect to his page (GET)
    else:
               
        rows = exe.execute("SELECT idphoto, location, url, weather, landscape FROM gallery WHERE \
                        idphoto = :idphoto",
                        {"idphoto": idphoto})
                        
        gallery = rows.fetchall()
        
        # to_char(time, 'DD Mon YY - HH24:MI:SS') as time \
        results = exe.execute("SELECT r.idphoto, r.timeDate, r.username, r.comment, r.rating \
                            FROM users u\
                            JOIN reviews r\
                            ON u.username = r.username \
                            WHERE r.idphoto = :idphoto \
                            ORDER BY r.timeDate desc",
                            {"idphoto": idphoto})
                            
        # ORDER BY time
        reviews = results.fetchall()
        
        return render_template("image.html", gallery=gallery, username=username, reviews=reviews)
    
if __name__ == "__main__":

    app.run(debug=True)

