# Budget50

## Web Application designed to keep track of income and expenses

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

## Database
The database used for this application is SQLite3 and contains 5 tables:
1. users: this stores the user's name, password (hash), and the total amount of both expenses and income
2. expense_categories: in this table are the expense categories that come by default when you create a new account and it also has the custom categories
3. expenses: this table contains every expense of every user and it has the date of the expense, the amount and the id of the category of the expense
4. income_categories: similar to expense_categories but for income categories
5. incomes: similar to expenses but for incomes



