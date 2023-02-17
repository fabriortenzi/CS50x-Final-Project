# Budget50

## Web Application to keep track of income and expenses

This project registers expenses or incomes and organizes them in categories. The user has to create an account in order to acces the platform and use the following features:

* See the current Balance (Total Income - Total Expenses)
* Add a new Expense or Income
* Create a new Category (for Expense or Income)
* Watch the percentage of each category for expenses (or incomes) with respect to the total amount of expenses (or incomes)

## Video Demo: 

## How to install the app

1. Clone this project
2. Open the folder's project with Visual Studio Code (in Windows Subsystem for Linux mode)
3. Install requirements: ```$ pip install -r requirements.txt```
4. Run the app: ```$ flask run```

## Application Design

## Name
The name is Budget50. Budget stands for the functionality of the app (is used to make a budget) and 50 to keep up with the theme of the course (througout the curse some apps had a 50 at the end of the name, expamples being check50, submit50 and debug50).

## Database
The database used for this application is SQLite3 and contains 5 tables:
1. users: this stores the user's name, password (hash), and the total amount of both expenses and income
2. expense_categories: in this table are the expense categories that come by default when you create a new account and it also has the custom categories
3. expenses: this table contains every expense of every user and it has the date of the expense, the amount and the id of the category of the expense
4. income_categories: similar to expense_categories but for income categories
5. incomes: similar to expenses but for incomes

## Layouts
The application is divided into two layouts. The first one "login-layout.html" is used for the login, signup, and every other page of the app that is a form. It was inspired from [this video](https://www.youtube.com/watch?v=B6e4Fg_-CXY) since it's modern and visually appealing.
The other layout "layout.html" contains a navbar with links to add expense, income and category and also log out. 
Every .html file of the app extends either "login-layout.html" or "layout.html". Each of these templates has their own CSS file because they have different properties regarding their elements, such as inputs, containers and buttons and also the positioning of those elements.

## Login and Signup
The login page extends "login-layout.html" and contains inputs for the username, password and a button to log in. It also has a link to the signup page to create an account.
The signup page also extends "login-layout.html" and contains inputs for the username, password, confirm the password and a button to create the account.

## Main page
The main page extends "layout.html" and contains the user's balance, total expenses, total income and also two buttons to show income or expenses by category. 

## Add Expense, Add Income and Add Category
Each of these files extends "login-layout.html". I decided to do so beacuse they are forms and since login and signup are also forms, those parts of the app will have a similar appearance.
Add Expense and Add Income contain inputs for the amount of money, a dropdown to select the category (made with JavaScript and CSS), the date and a button to submit. In Expense the button is red and in Income green.
Add Category contains inputs for the name, a color, a radio to choose type (expense or income) and the button to submit. 

## Show Expenses and Show Income
Each of these files extends "layout.html" and shows the percentage of each category of income (or expense) with respect to the total amount of income (or expense). Each category has a circular progress bar (made with CSS with the help of [this video](https://www.youtube.com/watch?v=8a9f8hG6M5A&t=13s)). 

The percentage is calculated in the backend by making a query to the database to select the categories and the also the total amount accumulated from each category. Each category is passed to "show-income.html" or "show-expenses.html" with the help of render_template() from Flask. That is because the percentage of each category is not static and needs to be updated each time that page is loaded. In short, a for loop is used in jinja syntax to plug in the actual values of the category (color and percentage of the circular bar to make the animation).
   




