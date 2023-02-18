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

        # Check for blank inputs
        if not username or not password:
            return render_template("error.html", message="Some inputs were left blank")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("error.html", message="Username does not exist")        
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="Incorrect password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]        

        # Redirect user to home page
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

        # Check for blank inputs
        if not username or not password or not confirmation:
            return render_template("error.html", message="Some inputs were left blank")

        # Check for unrepeated username and password's match
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return render_template("error.html", message="Username already exists")
        if password != confirmation:
            return render_template("error.html", message="Passwords no dot match")
        
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
                
        return redirect("/")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Main page"""

    # GET
    if request.method == "GET":

        # Get user's info
        record = db.execute("SELECT username, total_expenses, total_income FROM users WHERE id = ?", session["user_id"])
        
        # Show total expenses as a positive number
        record[0]["total_expenses"] = -int(record[0]["total_expenses"])
        
        return render_template("index.html", record=record)

    # POST
    else:

        type_button = request.form.get("type")

        # Check for blank inputs
        if not type_button:
            return render_template("error.html", message="Some inputs were left blank")

        if type_button == "expenses":
            return redirect("/show-expenses")
        elif type_button == "income":
            return redirect("/show-income")
        else:
            return render_template("error.html", message="Invalid Type")


@app.route("/show-expenses")
@login_required
def showExpenses():
    
    # Consult database for expense categories
    categories = db.execute("SELECT * FROM expense_categories WHERE user_id IS NULL OR user_id = ?", session["user_id"])
        
    for category in categories:
        category["percentage"] = 0
        category["degree"] = 0

    # Consult database for user's expenses
    expenses = db.execute("SELECT SUM(expenses.total) AS total, expense_categories.name, expense_categories.id FROM expenses JOIN expense_categories ON expenses.category_id = expense_categories.id WHERE expenses.user_id = ? GROUP BY category_id",
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

    return render_template("show-expenses.html", categories=categories)


@app.route("/add-expense", methods=["GET", "POST"])
@login_required
def expense():
    """Add an Expense"""

    # GET
    if request.method == "GET":

        # Get the expense categories
        categories = db.execute("SELECT * FROM expense_categories WHERE user_id IS NULL OR user_id = ? ORDER BY name",
                                session["user_id"])

        date = datetime.date.today()

        return render_template("add-expense.html", categories=categories, date=date)

    # POST
    else:
        amount = request.form.get("amount")
        category = request.form.get("category") 
        date = request.form.get("date")   

        # Check for blank inputs
        if not amount or not category or not date:
            return render_template("error.html", message="Some inputs were left blank")  
        
        # Convert amount to float
        try:
            amount = float(amount)
        except:
            return render_template("error.html", message="Amount is not a positive number")

        # Check if it is a positive number
        if amount <= 0:
            return render_template("error.html", message="Amount is not a positive number")
        
        amount = -int(amount)

        category_id = db.execute("SELECT id FROM expense_categories WHERE name = ? AND (user_id IS NULL or user_id = ?)", category, session["user_id"])
        category_id = category_id[0]["id"]

        db.execute("INSERT INTO expenses (date, total, user_id, category_id) VALUES(?, ?, ?, ?)",
                   date, amount, session["user_id"], category_id)
        
        db.execute("UPDATE users SET total_expenses = total_expenses + ? WHERE id = ?",
                   amount, session["user_id"])

        return redirect("/")   


@app.route("/show-income")
@login_required
def showIncome():
    """Show user's income"""

    # Consult database for income categories
    categories = db.execute("SELECT * FROM income_categories WHERE user_id IS NULL OR user_id = ?", session["user_id"])

    for category in categories:
        category["percentage"] = 0
        category["degree"] = 0

    # Consult database for user's income
    incomes = db.execute("SELECT SUM(incomes.total) AS total, income_categories.name, income_categories.id FROM incomes JOIN income_categories ON incomes.category_id = income_categories.id WHERE incomes.user_id = ? GROUP BY category_id",
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

    return render_template("show-income.html", categories=categories)


@app.route("/add-income", methods=["GET", "POST"])
@login_required
def income():
    """Add an Income"""

    # GET
    if request.method == "GET":

        # Get the income categories
        categories = db.execute("SELECT * FROM income_categories WHERE user_id IS NULL OR user_id = ? ORDER BY name",
                                session["user_id"])

        date = datetime.date.today()

        return render_template("add-income.html", categories=categories, date=date)

    # POST
    else:
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        
        # Check for blank inputs
        if not amount or not category or not date:
            return render_template("error.html", message="Some inputs were left blank")  
        
        # Convert amount to float
        try:
            amount = float(amount)
        except:
            return render_template("error.html", message="Amount is not a positive number")

        # Check if it is a positive number
        if amount <= 0:
            return render_template("error.html", message="Amount is not a positive number")

        category_id = db.execute("SELECT id FROM income_categories WHERE name = ? AND (user_id IS NULL or user_id = ?)", category, session["user_id"])
        category_id = category_id[0]["id"]

        db.execute("INSERT INTO incomes (date, total, user_id, category_id) VALUES(?, ?, ?, ?)",
                   date, amount, session["user_id"], category_id)
        
        db.execute("UPDATE users SET total_income = total_income + ? WHERE id = ?",
                   amount, session["user_id"])

        return redirect("/")   
    

@app.route("/add-category", methods=["GET", "POST"])
@login_required
def category():
    """Add custom category"""

    # GET
    if request.method == "GET":
        return render_template("add-category.html")
    
    # POST
    else:
        name = request.form.get("name")
        color = request.form.get("color")
        type_cat = request.form.get("type")

        if not name or not color or not type_cat:
            return render_template("error.html", message="Some inputs were left blank")
        
        name = capwords(name) 

        # Record Category
        if type_cat == "expense":
            # Check if the category was previously added
            if not db.execute("SELECT id FROM expense_categories WHERE name = ? AND user_id = ?", name, session["user_id"]):
                db.execute("INSERT INTO expense_categories (name, icon, color, user_id) VALUES(?, ?, ?, ?)", 
                           name, "add", color, session["user_id"]) 
            else:
                return render_template("error.html", message="The Category was already added")
        elif type_cat == "income":
            # Check if the category was previously added
            if not db.execute("SELECT id FROM income_categories WHERE name = ? AND user_id = ?", name, session["user_id"]):
                db.execute("INSERT INTO income_categories (name, icon, color, user_id) VALUES(?, ?, ?, ?)", 
                           name, "add", color, session["user_id"]) 
            else:
                return render_template("error.html", message="The Category was already added")
        else:
            return render_template("error.html", message="Incorrect Type")        

        return redirect("/")    


@app.route("/history")
@login_required
def history():
    """Show user's records"""

    # Consult database to find user's expenses and incomes
    records = db.execute("SELECT expenses.date, expense_categories.name, expenses.total, expense_categories.icon FROM expenses JOIN expense_categories ON expense_categories.id = expenses.category_id WHERE expenses.user_id = ? UNION SELECT incomes.date, income_categories.name, incomes.total, income_categories.icon FROM incomes JOIN income_categories ON income_categories.id = incomes.category_id WHERE incomes.user_id = ? ORDER BY date DESC", session["user_id"], session["user_id"])

    date = datetime.date.today()

    return render_template("history.html", records=records, date=date)

