import sqlite3
import datetime

# conn = sqlite3.connect('finance.db')
# db = conn.cursor()

# #find id of logged on user
# id = 4

# #retive cash balance of logged on user
# db.execute('''SELECT * FROM users WHERE id=?''', (id,))
# rows = db.fetchone()
# print(rows[3])

#establish connection to database
# conn = sqlite3.connect('finance.db')
# db = conn.cursor()


# try:
#     db.execute('''SELECT * FROM transactions WHERE userid=? ORDER BY Symbol''', (4,))
#     rows = db.fetchall()
    
#     #close database connection    
#     conn.commit()
#     conn.close()
#     for r in rows:
#         x=0
#         if x=0
#             r[0] = 
#         if r[0] == r[]
#             r[4] = t
#         print(r)           

# except sqlite3.Error as er:
#     print(er)

# conn.close()


from collections import namedtuple  
from itertools import groupby

#a namedtuple is a tuple that permits attribute access. 
#In this case, beer.category maps to beer[0], and 
#beer.brand maps to beer[0]   
Beer = namedtuple('Beer', ['category', 'brand'])

# Note that the beers array is sorted   
beers = [  
    Beer('IPA', 'Sierra Nevada'),  
    Beer('IPA', 'Goose Island'),  
    Beer('Porter', 'Deschutes Black Butte'),  
    Beer('Porter', 'Stone Smoked Porter'),  
    Beer('Pilsener', 'Sierra Nevada Pilsener'),  
    Beer('Pilsener', 'Pilsener Urquell')  
]

beer_map = {}  
for key, group in groupby(beers, lambda beer: beer.category):  
    beer_map[key] = [beer.brand for beer in group]

# Or, preferably using dict comprehensions:  
beer_map = {
    key: [beer.brand for beer in group] 
    for key, group in groupby(beers, lambda beer: beer.category)
}

print (beer_map) 