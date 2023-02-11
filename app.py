import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from string import capwords
import datetime

from helpers import login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


# Key function to sort categories by percentage
def get_percentage(record):
    return record.get('percentage')


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
    
    # Consult database for expense categories
    categories = db.execute("SELECT * FROM expense_categories")

    for category in categories:
        category["percentage"] = 0
        category["degree"] = 0

    # Consult database for user's expenses
    expenses = db.execute("SELECT SUM(expenses.total) AS total, expense_categories.name, expense_categories.id FROM expenses JOIN expense_categories ON expenses.category_id = expense_categories.id WHERE user_id = ? GROUP BY category_id",
                          session["user_id"])
    
    # Calculate percentage of each category
    sum = 0
    for i in range(len(expenses)):
        sum += expenses[i]["total"]

    for i in range(len(expenses)):
        expenses[i]["total"] = round(((expenses[i]["total"] / sum) * 100), 1)

    for expense in expenses:
        for category in categories:
            if expense["id"] == category["id"]:
                category["percentage"] = expense["total"]
                category["degree"] = round(((category["percentage"] / 100) * 180), 1)
                break

    categories.sort(key=get_percentage, reverse=True)

    return render_template("index.html", categories=categories)


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
        categories = db.execute("SELECT * FROM expense_categories ORDER BY name")

        date = datetime.date.today()

        return render_template("expense.html", categories=categories, date=date)

    # POST
    else:
        amount = request.form.get("amount")
        category = request.form.get("category")    

        print(amount, category)

        return redirect("/")    


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """Add an Income"""

    # GET
    if request.method == "GET":

        # Get the income categories
        categories = db.execute("SELECT * FROM income_categories ORDER BY name")

        return render_template("income.html", categories=categories)

    # POST
    else:
        amount = request.form.get("amount")
        category_id = request.form.get("category")
        date = request.form.get("date")

        # Record the income
        db.execute("INSERT INTO incomes (date, total, user_id, category_id) VALUES(?, ?, ?, ?)",
                   date, amount, session["user_id"], category_id)
        
        # Update user's cash
        db.execute("UPDATE users SET balance = balance + ? WHERE id = ?", amount, session["user_id"])
        db.execute("UPDATE users SET total_income = total_income + ? WHERE id = ?", amount, session["user_id"])

        return redirect("/balance")


@app.route("/balance")
@login_required
def balance():
    """Show user's balance"""

    # Get user's balance
    balance = db.execute("SELECT balance FROM users WHERE id = ?", session["user_id"])
    balance = balance[0]["balance"]

    # Get user's total income and expenses
    income_number = db.execute("SELECT total_income FROM users WHERE id = ?", session["user_id"])
    income_number = income_number[0]["total_income"]
    expenses = db.execute("SELECT total_expenses FROM users WHERE id = ?", session["user_id"])
    expenses = expenses[0]["total_expenses"]

    # Consult database for income categories
    categories = db.execute("SELECT * FROM income_categories")

    for category in categories:
        category["percentage"] = 0
        category["degree"] = 0

    # Consult database for user's income
    incomes = db.execute("SELECT SUM(incomes.total) AS total, income_categories.name, income_categories.id FROM incomes JOIN income_categories ON incomes.category_id = income_categories.id WHERE user_id = ? GROUP BY category_id",
                          session["user_id"])
    
    # Calculate percentage of each category
    sum = 0
    for i in range(len(incomes)):
        sum += incomes[i]["total"]

    for i in range(len(incomes)):
        incomes[i]["total"] = round(((incomes[i]["total"] / sum) * 100), 1)

    for income in incomes:
        for category in categories:
            if income["id"] == category["id"]:
                category["percentage"] = income["total"]
                category["degree"] = round(((category["percentage"] / 100) * 180), 1)
                break

    categories.sort(key=get_percentage, reverse=True)

    return render_template("balance.html", balance=balance, income_number=income_number, expenses=expenses, categories=categories)


@app.route("/history")
@login_required
def history():
    """Show user's records"""

    # Consult database to find user's expenses and incomes
    records = db.execute("SELECT expenses.date, expense_categories.name, expenses.total, expense_categories.icon FROM expenses JOIN expense_categories ON expense_categories.id = expenses.category_id WHERE user_id = ? UNION SELECT incomes.date, income_categories.name, incomes.total, income_categories.icon FROM incomes JOIN income_categories ON income_categories.id = incomes.category_id WHERE user_id = ? ORDER BY date DESC", session["user_id"], session["user_id"])

    date = datetime.date.today()

    return render_template("history.html", records=records, date=date)


@app.route("/category", methods=["GET", "POST"])
@login_required
def category():
    """Add custom category"""

    # GET
    if request.method == "GET":
        return render_template("category.html")
    
    # POST
    else:
        name = request.form.get("name")
        color = request.form.get("color")
        type_cat = request.form.get("type")

        #if not name or not color or not type_cat:
            #return render_template("error.html", message="Some inputs were left blank")
        
        name = capwords(name)

        # Record Category
        if type_cat == "expense":
            db.execute("INSERT INTO expense_categories (name, icon, color, user_id) VALUES(?, ?, ?, ?)", 
                       name, "add", color, session["user_id"])     
        elif type_cat == "income":
            db.execute("INSERT INTO income_categories (name, icon, color, user_id) VALUES(?, ?, ?, ?)", 
                       name, "add", color, session["user_id"]) 
        #else:
            #return render_template("error.html", message="Incorrect Type")        

        return redirect("/")
    
