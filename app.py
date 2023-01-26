import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # GET
    if request.method == "GET":
        return render_template("login.html")
    
    # POST
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]        

        # Redirect user to home page
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Create account"""

    # GET
    if request.method == "GET":
        return render_template("/signup.html")

    # POST
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return redirect("/")
            # Complete

        if password != confirmation:
            return redirect("/")
            # Complete
        
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
                
        return redirect("/")


@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    """Add an Expense"""

    # GET
    if request.method == "GET":

        # Get the expense categories
        categories = db.execute("SELECT name FROM expense_categories")

        list_categories = []
        for i in range(len(categories)):
            list_categories.append(categories[i]['name'])
        
        return render_template("expense.html", categories=list_categories)

    # POST