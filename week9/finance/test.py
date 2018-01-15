import sqlite3
import datetime
from helpers import *

#establish connection to database
conn = sqlite3.connect('finance.db')
db = conn.cursor()


try:
    #check if stock is already owned and add adds to shares
    
    #retrive tranaction history
    db.execute('''SELECT * FROM portfolio WHERE UserID=? and symbol=?''', (4, "AMD"))
    port_info = db.fetchone()
    db.close()

    print(port_info)

        
    #close database connection    
    conn.commit()
    conn.close()

except sqlite3.Error as er:
    print(er)

conn.close()

# from pinance import Pinance

# symbol = "msft"
# stock = Pinance(symbol)
# stock.get_quotes()
# print(stock.quotes_data)