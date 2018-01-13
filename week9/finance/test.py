import sqlite3
import datetime

#establish connection to database
conn = sqlite3.connect('finance.db')
db = conn.cursor()


try:
    #check if stock is already owned and add adds to shares
    
    db.execute('''SELECT * FROM portfolio WHERE UserID=?''', (4,))
    port_info = db.fetchall()

    print(port_info[0][1])
    #close database connection    
    conn.commit()
    conn.close()

except sqlite3.Error as er:
    print(er)

conn.close()

