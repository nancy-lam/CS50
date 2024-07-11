import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    # Get user's stocks and shares
    stocks = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transactions \
                        WHERE user_id = :user_id \
                        GROUP BY symbol \
                        HAVING total_shares > 0", user_id=user_id)

    # Get user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]['cash']

    # Total value of all stock holdings and cash
    sum = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["symbol"] = quote["symbol"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["total_shares"]
        sum += stock["total"]

        # convert price and total to usd format
        stock["price"] = usd(stock["price"])
        stock["total"] = usd(stock["total"])

    return render_template("index.html", stocks=stocks, cash=usd(cash), sum=usd(sum))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    user_id = session["user_id"]

    # User reached route via POST
    if request.method == "POST":

        # Put input of user in variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # User the lookup() function
        quote = lookup(symbol)

        # Check for user error
        if not symbol or quote is None:
            return apology("symbol not found")
        elif not shares or not shares.isdigit():
            return apology("Missing/Invalid shares")

        shares = int(shares)
        if shares <= 0:
            return apology("invalid shares")

        cash = db.execute("SELECT cash FROM users WHERE id =?", user_id)[0]['cash']

        price = quote['price']
        total_cost = price * shares

        if cash < total_cost:
            return apology("Not enough cash!")
        else:
            balance = cash - total_cost
            # Update the users table after the user bought stock/stocks
            db.execute("UPDATE users SET cash = :balance WHERE id = :user_id",
                       balance=balance, user_id=user_id)

            # Add the purchase into the history table
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, method) VALUES (:user_id, :symbol, :shares, :price, 'Buy')",
                       user_id=user_id, symbol=quote["symbol"], shares=shares, price=price)

            flash(f"Bought {shares} shares of {quote['symbol']} for {usd(total_cost)}")

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC", user_id=user_id)

    # return history template
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Invalid symbol", 400)
        quote['price'] = usd(quote['price'])
        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("This username is already taken", 400)

        # Convert password to hash
        hash = generate_password_hash(password)

        # Insert into the username table the registered username and hash password
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    cash = db.execute("SELECT cash FROM users WHERE id =?", user_id)[0]['cash']

    stocks = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transactions \
                        WHERE user_id = :user_id \
                        GROUP BY symbol \
                        HAVING total_shares > 0", user_id=user_id)

    # User reached route via POST
    if request.method == "POST":

        # Put input of user in variables
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("must provide symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must provide a positive integer number of shares")
        else:
            shares = int(shares)

        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["total_shares"] < shares:
                    return apology("Not enough shares!")
                else:
                    # User the lookup() function
                    quote = lookup(symbol)

                    if quote is None:
                        return apology("symbol not found")
                    price = quote["price"]
                    total_sales = shares * price
                    balance = cash + total_sales

                    # Update the users table after the user bought stock/stocks
                    db.execute("UPDATE users SET cash = :balance WHERE id = :user_id",
                               balance=balance, user_id=user_id)

                    # Add the purchase into the history table
                    db.execute("INSERT INTO transactions (user_id, symbol, shares, price, method) VALUES (:user_id, :symbol, :shares, :price, 'Sell')",
                               user_id=user_id, symbol=symbol, shares=-shares, price=price)

                    flash(f"Sold {shares} shares of {quote['symbol']} for {usd(total_sales)}")

                    return redirect("/")

    else:
        return render_template("sell.html")
