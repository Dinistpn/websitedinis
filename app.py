import os, json
import requests
import datetime
import secrets

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session 
from flask_session import Session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)

if not os.getenv('DATABASE_URL', None):
    raise RuntimeError("DATABASE_URL is not set")

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))

exe = scoped_session(sessionmaker(bind=engine))

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))  

@app.route("/", methods=['GET', 'POST'])    
def index():

    if request.method == "POST":
        """ Show search box """
        location=request.form.get("location")
        days= request.form.get("days")
        exe.execute("INSERT INTO destinations (location, days) VALUES (:location,:days )",
                                {"location":location,
                                "days":days})
            # Commit changes to database
        exe.commit()
   
        flash('Submited', 'info')

        # Redirect user to index
        return redirect(request.referrer)
    dest=exe.execute("select * from destinations order by id Desc LIMIT 6;")

    destinations= dest.fetchall()
  
    return render_template("index.html", destinations=destinations)

@app.route("/restrict", methods=['GET', 'POST'])    
def restrict():

    """ Show search box """
    #username = session.get('username')
    
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
    
    return render_template("restrict.html", landscape=landscape, maxP=maxP, 
    recent=recent, weather=weather)

@app.route("/draws", methods=['GET', 'POST'])
def draws():  
    
    #username = session.get('username')
        
    return render_template("draws.html", )
    
@app.route("/results", methods=['GET', 'POST'])
def results():

    #username = session.get('username')
    
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
    
    
    
    return render_template("results.html", gallery=gallery)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Query database for username
        userCheck = exe.execute("SELECT * FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchone()

        # Check if username already exist
        if userCheck:
            return render_template("error.html", message="username already exist")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Ensure confirmation wass submitted 
        elif not request.form.get("confirmation"):
            return render_template("error.html", message="must confirm password")

        # Check passwords are equal
        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("error.html", message="passwords didn't match")
        
        # Hash user's password to store in DB
        
        hashed_pass = generate_password_hash(request.form.get("password"), method='pbkdf2:sha512', salt_length=8)
        # Insert register into DB
        exe.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                            {"username":request.form.get("username"), 
                             "password":hashed_pass})

        # Commit changes to database
        exe.commit()

        flash('Account created', 'info')

        # Redirect user to login page
        return redirect(url_for('login'))
        
    else:
        return render_template("registration.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    #session.clear()

    username = request.form.get("username")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Query database for username (http://zetcode.com/db/sqlalchemy/rawsql/)
        # https://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
        rows = exe.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username})
        
        result = rows.fetchone()

        # Ensure username exists and password is correct
        if result == None or not check_password_hash(result[2], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["username"] = request.form.get("username")

        # Redirect user to home page
        return redirect("/restrict")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
def loggedout():
    session.pop('username', None)
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
    
@app.route("/image/<idphoto>", methods=['GET', 'POST']) 
def image(idphoto):
    
    username = session.get('username')
        
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
        
        return render_template("image.html", gallery=gallery, username=session.get('username'), reviews=reviews)

if __name__ == "__main__":

    app.run(debug=True)
