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

    db.execute('''SELECT * FROM portfolio WHERE UserID=? and shares > 0''', (id,))
    port_info = db.fetchall()

    j_list=[] 
    total_share=0

    for p in port_info:
        j_stock = p[1]
        j_share = p[2]
        j_name = p[3]
        j_result = lookup(j_stock)
        j_price = j_result['price']
        j_shares_valuei = j_price * j_share
        j_shares_value = usd(j_price * j_share)
        j_price = usd(j_price)
        j_tuple = (j_stock, j_share, j_name, j_price, j_shares_value)
        j_list.append(j_tuple)
        total_share = total_share + j_shares_valuei
    
    total_v = total_share + rows[3]
    conn.close()
    if len(port_info) > 0:
        return render_template("index.html", cash=usd(rows[3]), data=j_list, total_value=usd(total_v), user=rows[1])
    else:
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
                ent_sym = qt_result1['symbol']
                db.execute('''SELECT * FROM portfolio WHERE UserID=? and symbol=?''', (id, ent_sym))
                db_port = db.fetchall()
                
                #check if user has shares of stock then either update shares or insert new record
                if len(db_port) > 0:
                    db.execute('''UPDATE portfolio SET shares = shares + ? WHERE UserID = ? and symbol = ?''', (request.form.get("Quantity"), id, ent_sym))
                else:
                    db.execute('''INSERT INTO portfolio (Symbol, Name, shares, UserID) VALUES(?,?,?,?)''', 
                    (qt_result1['symbol'], qt_result1['name'], request.form.get("Quantity"), id))

                #close database connection    
                conn.commit()
                conn.close()

            except sqlite3.Error as er:
                return apology(er)
        
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
    
    id = session['user_id']

    #establish connection to database
    conn = sqlite3.connect('finance.db')
    db = conn.cursor()

    #retrive current user id
    db.execute('''SELECT * FROM users WHERE id=?''', (id,))
    rows = db.fetchone()

    db.execute('''SELECT * FROM transactions WHERE UserID=?''', (id,))
    trans_info =db.fetchall()
    db.close()

    t_list = []
    
    for t in trans_info:
        t_stock = t[0]
        t_name = t[1]
        t_date = date_f(t[2])
        t_price = t[3]
        t_share = t[4]
        t_tuple = (t_stock ,t_name,t_date,t_price,t_share)
        t_list.append(t_tuple)
        
    #retrieve all trans actions for current user
    return render_template("history.html", data = t_list, user=rows[1])


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
            session['pass_symbol'] = qt_result['symbol']
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

    id = session['user_id']

    if request.method == "POST":

        # ensure sell is not 0

        conn = sqlite3.connect('finance.db')
        db = conn.cursor()

        db.execute('''SELECT * FROM portfolio WHERE UserID=? and symbol=?''', (id, request.form.get("symbol").upper()))
        port_info = db.fetchone()
        
        if request.form.get("sell_qty") == 0:
            return apology("Cannot sell 0")

        if int(request.form.get("sell_qty")) > port_info[2]:
            return apology("Trying to sell more share than you have")
                
        else:
            try:
                #Get current date and time
                now = datetime.datetime.now()

                #conver to formated string
                date_time = now.strftime("%Y%m%d%H%M%S")

                qt_result2 = lookup(request.form.get("symbol"))
                
                #insert transaction into table
                db.execute('''INSERT INTO transactions(Symbol, Name, Date, Price, qty, UserID) VALUES(?,?,?,?,?,?)''', 
                (request.form.get("symbol").upper(), qt_result2['name'], date_time, qt_result2['price'], -int(request.form.get("sell_qty")), id))

                #update users cash
                db.execute('''UPDATE users SET cash = cash + ? WHERE id = ?''', ((qt_result2['price']*float(request.form.get("sell_qty"))), id))

                db.execute('''UPDATE portfolio SET shares = shares - ? WHERE UserID = ? and symbol = ?''', (int(request.form.get("sell_qty")), id, request.form.get("symbol").upper()))

                #close database connection    
                conn.commit()
                conn.close()

                # redirect user to home page
                return redirect(url_for("index"))

            except sqlite3.Error as er:
                return apology(er)

    else:
        #establish connection to database
        conn = sqlite3.connect('finance.db')
        db = conn.cursor()

        #retrive tranaction history
        db.execute('''SELECT * FROM transactions WHERE UserID=? and qty > 0''', (id,))
        trans_info =db.fetchall()
        db.close()

        j_list=[] 

        for p in trans_info:
            j_stock = p[0]
            j_share = p[4]
            j_name = p[1]
            j_purchase_price = usd(p[3])
            j_result = lookup(j_stock)
            j__current_price = j_result['price']
            j__current_price_usd = usd(j__current_price)
            j_tuple = (j_stock, j_name, j_purchase_price, j_share, j__current_price_usd)
            j_list.append(j_tuple)

        #retrieve all trans actions for current user
        return render_template("sell.html", data = j_list, lng= len(trans_info))

@app.route("/sp500", methods=["GET"])
@login_required
def sp500():
    """List of S&P500 companies."""
    return render_template("sp500.htm")    