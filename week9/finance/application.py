import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.context import CryptContext
from tempfile import mkdtemp
import datetime
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#setup established hasing scheme
myctx = CryptContext(schemes=["sha256_crypt"])
# configure CS50 Library to use SQLite database
#db = SQL("sqlite:///finance.db")

# https://docs.python.org/3/library/sqlite3.html
# conn = sqlite3.connect('finance.db')
# db = conn.cursor()

@app.route("/")
@login_required
def index():
    
    id = session['user_id']

    #establish connection to database
    conn = sqlite3.connect('finance.db')
    db = conn.cursor()

    #retrive current user id
    db.execute('''SELECT * FROM users WHERE id=?''', (id,))
    rows = db.fetchone()

    #retrieve all trans actions for current user
    
    conn.close()

    return render_template("index.html", cash=rows[3])

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    if request.method == "POST":
       
        # ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide Stock symbol")

        #lookup stock
        qt_result1 = lookup(request.form.get("symbol"))
        if qt_result1 == None:
            return apology("Stock symbol entered not found")
        
        #establish connection to database
        conn = sqlite3.connect('finance.db')
        db = conn.cursor()

        #find id of logged on user
        id = session['user_id']

        #retive cash balance of logged on user
        db.execute('''SELECT * FROM users WHERE id=?''', (id,))
        rows = db.fetchone()

        #check is user has enough money
        if (qt_result1['price']*float(request.form.get("Quantity"))) > rows[3]:
            #return error message with current cash and purchase price
            return render_template("funds.html", Balance=rows[3], total_price=(qt_result1['price']*float(request.form.get("Quantity"))))
        
        else:
            try:
                #Get current date and time
                now = datetime.datetime.now()
                
                #conver to formated string
                date_time = now.strftime("%Y%m%d%H%M%S")
                
                #insert transaction into table
                db.execute('''INSERT INTO transactions(Symbol, Name, Date, 
                    Price, qty, UserID) VALUES(?,?,?,?,?,?)''', (qt_result1['symbol'], qt_result1['name'], 
                    date_time, qt_result1['price'], request.form.get("Quantity"), id))
                
                #update users cash
                db.execute('''UPDATE users SET cash = cash - ? WHERE id = ?''', 
                ((qt_result1['price']*float(request.form.get("Quantity"))), id))

                #check if stock is already owned and add adds to shares
                ent_sym = request.form.get("symbol")
                db.execute('''SELECT * FROM portfolio WHERE UserID=? and symbol=?''', (id, ent_sym))
                db_port = db.fetchall()
                
                if db_port > 0:
                    db.execute('''UPDATE portfolio SET shares = share - ? WHERE id = ? and symbol=?''', 
                    (request.form.get("Quantity"), id, ent_sym))
                else:
                    db.execute('''INSERT INTO portfolio (Symbol, Name, shares, UserID) VALUES(?,?,?,?)''', 
                    (qt_result1['symbol'], qt_result1['name'], request.form.get("Quantity"), id))

                #close database connection    
                conn.commit()
                conn.close()

            except:
                return apology("Error registering transaction, Please try again")
        
        # redirect user to home page
        return redirect(url_for("index"))        
  
    else:
        return render_template("buy.html")

@app.route("/funds", methods=["POST"])
@login_required
def funds():
    """Buy shares of stock."""

    if request.method == "POST":
        return render_template("buy.html", sy)

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    conn = sqlite3.connect('finance.db')
    db = conn.cursor()

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        username = request.form.get("username")

        # query database for username
        db.execute('''SELECT * FROM users WHERE username=?''', (username,))
        rows = db.fetchone()

        # ensure username exists and password is correct
        if rows is None or not myctx.verify(request.form.get("password"), rows[2]):
            return apology("invalid username and/or password")

        #close database connection    
        conn.close()

        # remember which user has logged in
        session["user_id"] = rows[0]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        #retrive stock quote
        qt_result = lookup(request.form.get("symbol"))
        if qt_result == None:
            return apology("Stock symbol entered not found")

        else:
            #session['pass_symbol'] = qt_result['symbol']
            session['pass_symbol'] = "MSFT"
             #return apology("Stock symbol entered not found")
            return render_template("show_quote.html", name=qt_result['name'], price=qt_result['price'], symbol=qt_result['symbol'])
    else:
        return render_template("quote.html")
    

@app.route("/show_quote", methods=["POST"]) # can only get here via post.
@login_required
def show_quote():
    """Display stock quote."""

    pass_symbol = session['pass_symbol']

    if request.method == "POST":
        return render_template("buy.html", symbol=pass_symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    conn = sqlite3.connect('finance.db')
    db = conn.cursor()

    # forget any user_id
    session.clear()
    
    #return render_template("register.html")

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password confirmation was submitted
        elif not request.form.get("conf_password"):
            return apology("must complete password confirmation Field")

        # ensure password confirmation matched password
        elif request.form.get("password") != request.form.get("conf_password"):
            return apology("password and password confirmation fields do not match")

        
        #hash userpassword using werkzeug.security import generate_password_hash
        hash_pw = myctx.hash(request.form.get("password"))
        username = request.form.get("username")

        # Add user to users table
        #result = db.execute('''INSERT INTO users(username, hash) VALUES(?,?)''', (username, hash_pw))

        try:
            db.execute('''INSERT INTO users(username, hash) VALUES(?,?)''', (username, hash_pw))
        except:
            return apology("Username already exists")

        # query database for username
        db.execute('''SELECT * FROM users WHERE username=?''', (username,))
        rows = db.fetchone()
        
        #commit changes and close database    
        conn.commit()
        conn.close()
        
        # remember which user has logged in
        session["user_id"] = rows[0]

        # redirect user to home page
        return redirect(url_for("index"))


    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    return apology("TODO")
