from urllib.request import Request, urlopen
import requests
import json
from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# import demjson
import sys
import re
import datetime

import csv
def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
    #     Escape special characters.

    #     https://github.com/jacebrowning/memegen#special-characters
    #     """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
    # return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # reject symbol if it contains comma
    if "," in symbol:
        return None

    
    try:

        #code snippet taken from https://github.com/neberej/pinance
        
        url = 'https://finance.google.com/finance?output=json&q=%s' % symbol

        req = Request(url)
        resp = urlopen(req)
        content = resp.read().decode('ascii', 'ignore').strip()
        content = json.loads(content[3:])
        id = content[0]["id"]

        url1 = 'https://finance.google.com/finance/data?dp=mra&output=json&catid=all&cid=%s' % id

        req = Request(url)
        resp = urlopen(req)
        content = resp.read().decode('ascii', 'ignore').strip()
        content = json.loads(content[3:])


        # # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        # return {
        #     #"name":nm_stk,
        #     "name": symbol.upper(), # for backward compatibility with Yahoo
        #     "price": nm_price,
        #     "symbol": symbol.upper()
        # }

        # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            
            "name": content[0]["name"], # for backward compatibility with Yahoo
            "price": float(content[0]["l"]),
            "symbol": content[0]["symbol"].upper()
        }


    except:
        return None


def usd(value):
    """Formats value as USD."""
    return f"${value:,.2f}"

def date_f(d_val):
    """Formats the Date"""
    #take string date format and makes into date time
    dt=datetime.datetime.strptime(d_val,"%Y%m%d%H%M%S")
    #rearranges date
    dt_u = datetime.datetime.strftime(dt,"%c")
    return dt_u