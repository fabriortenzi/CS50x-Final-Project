# Budget50

## Web Application to keep track of income and expenses

This project registers expenses or incomes and organizes them in categories. The user has to create an account in order to acces the platform and use the following features:

* See the current Balance (Total Income - Total Expenses)
* Add a new Expense or Income
* Create a new Category (for Expense or Income)
* Watch the percentage of each category for expenses (or incomes) with respect to the total amount of expenses (or incomes)
* Watch a history of income and expenses

## Video Demo: https://youtu.be/A4t56DLA5Ys

## How to install the app

Prerequisites:
* Python v3.9.5 (or higher)

Steps:

1. Download the project's folder
2. Open the folder and then right click and select open with terminal
3. Run this command: ```pip install -r requirements.txt``` and wait until the installation is competed
4. Run this command: ```python app.py```
5. Run this command: ```flask run```
6. Click on the link that's right after running on (http://.....)
7. Use the app
8. Close terminal and browser

## Application Design

## Name
The name is Budget50. Budget stands for the functionality of the app (is used to make a budget) and 50 to keep up with the theme of the course (througout the curse some apps had a 50 at the end of the name, expamples being check50, submit50 and debug50).

## Database (budget.db)
The database used for this application is SQLite3 and contains 5 tables:
1. users: this stores the user's name, password (hash), and the total amount of both expenses and income
2. expense_categories: in this table are the expense categories that come by default when you create a new account and it also has the users' custom categories
3. expenses: this table contains every expense of every user and it has the date of the expense, the amount and the id of the category of the expense
4. income_categories: similar to expense_categories but for income categories
5. incomes: similar to expenses but for incomes

## Layouts
The application is divided into two layouts. The first one "login-layout.html" is used for the login, signup, and every other page of the app that is a form. It was inspired from [this video](https://www.youtube.com/watch?v=B6e4Fg_-CXY) since it's modern and visually appealing.
The other layout "layout.html" contains a navbar with links to add expense, income and category and also log out. 
Every .html file of the app extends either "login-layout.html" or "layout.html". Each of these templates has their own CSS file because they have different properties regarding their elements, such as inputs, containers and buttons and also the positioning of those elements.

## login.html and signup.html
The login page extends "login-layout.html" and contains inputs for the username, password and a button to log in. It also has a link to the signup page to create an account.
The signup page also extends "login-layout.html" and contains inputs for the username, password, confirm the password and a button to create the account.

## Main page (index.html)
The main page extends "layout.html" and contains the user's balance, total expenses, total income and also two buttons to show income or expenses by category. 

## add-expense.html, add-income.html and add-category.html
Each of these files extends "login-layout.html". I decided to do so beacuse they are forms and since login and signup are also forms, those parts of the app will have a similar appearance.
Add Expense and Add Income contain inputs for the amount of money, a dropdown to select the category (made with JavaScript and CSS), the date and a button to submit. In Expense the button is red and in Income green.
Add Category contains inputs for the name, a color, a radio to choose type (expense or income) and the button to add it. 

## show-expenses.html and show-income.html
Each of these files extends "layout.html" and shows the percentage of each category of income (or expense) with respect to the total amount of income (or expense). Each category has a circular progress bar (made with CSS with the help of [this video](https://www.youtube.com/watch?v=8a9f8hG6M5A&t=13s)). 

The percentage is calculated in the backend by making a query to the database to select the categories and the also the total amount accumulated from each category. Each category is passed to "show-income.html" or "show-expenses.html" with the help of render_template() from Flask. That is because the percentage of each category is not static and needs to be updated each time that page is loaded. In short, a for loop is used in jinja syntax to plug in the actual values of the category (color and percentage of the circular bar to make the animation).

## history.html
History extends "layout.html" and cointains every expense and income the user entered. To achive this, in the backend file (app.py) the data is consulted from the 2 tables (incomes and expenses) and then joined into one list to pass to "history.html" with render_template(). Inside history, a if statemtent makes the row color change if the amount is less than 0 to red and if it's greater than 0 to green.

## Backend (app.py)
app.py is the backend file to manage the http request and responses and it also contains the configuration of the database. The framework used to make this file is Flask.
Each element of the page is organized into @app.route modules. The modules that need to consult the database to then pass onto the .html file do so with the .execute() method. 
Every form that it's submitted to app.py is validated and returns an error if it's incorrect or if it's left blank. In addition, the inputs are also being validated from the part of the client.

## error.html
This file displays the error message when app.py detects an invalid input. It has a placeholder inside the file in jinja syntax for the message. Every time the server detects and error it returns "error.html" with render_template() and the placeholder for the message. 

## dropdown.js
Code to make the dropdown make in html work and also change the focus when the dropdown is clicked and return to normal when the option was selected.





